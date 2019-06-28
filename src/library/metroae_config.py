from ansible.module_utils.basic import AnsibleModule
import os
import io
import urllib3
import bambou
import logging
import sys
sys.path.insert(0, '/home/caso/dev/research/levistate/')
from configuration import Configuration
from errors import LevistateError
from template import TemplateStore
from user_data_parser import UserDataParser
from vsd_writer import VsdWriter, SOFTWARE_TYPE

urllib3.disable_warnings()

STATE_PRESENT = "present"      # for update/create
STATE_ABSENT = "absent"        # for revert
LEVISTATE_VERSION = "1.0"


DOCUMENTATION = '''
---
module: metroae_config
short_description: Apply/Revert a template-based configuration to the VSD
options:
  spec_path:
    description:
      - The path to the folder containing the specification of API for VSD
    required: true
    default: null
  template_path:
    description:
      - The path to the folder containing the templates
    required: true
    default: null
  user_data_path:
    description:
      - File or path containing the user data to be applied to the VSD.  Alternatively, a template and variables can be specified.
    required: false
    default: null
  template_name:
    description:
      - Name of template to apply configs.  Alternatively, user_data_path file can be used.
    required: false
    default: null
  variables:
    description:
      - List of dictionaries of variable/values sets to apply to template.  Alternatively, user_data_path file can be used.
    required: false
    default: null
  credentials:
    description:
    - A dictionary of credentials.
    - 'The following parameter is required:'
    - ' - username: (string): Username to log into the VSD.'
    - ' - password: (string): Password to log into the VSD.'
    - ' - enterprise: (string): Enterprise for VSD'
    - ' - url: (string): Url where the VSD can be reached'
    - ' - certificate: (string): Certificate file for VSD authentication'
    - ' - certificate_key: (string): Certificate key file for VSD authentication'
    type: dict
    default: {
        username: 'csproot',
        password: 'csproot',
        enterprise: 'csp',
        url: null
    }
    required: true
  state:
    description:
      - Apply/Update or revert the configuration on VSD
    required: true
    default: null
    choices: [ "present", "absent" ]
'''

class CustomLogHandler(logging.StreamHandler):

    def __init__(self, stream=None):
        if stream is not None:
            super(CustomLogHandler, self).__init__(stream)
        else:
            super(CustomLogHandler, self).__init__()

    def emit(self, record):
        saved_message = record.msg
        messages = record.msg.split('\n')
        for message in messages:
            record.msg = message
            super(CustomLogHandler, self).emit(record)
        record.msg = saved_message

class MetroaeConfig(object):
    def __init__(self,module):
        self.spec_path = module.params['spec_path']
        self.template_path = module.params['template_path']
        self.user_data_path = module.params['user_data_path']
        self.template_name = module.params['template_name']
        self.variables = module.params['variables']
        self.credentials = module.params['credentials']
        self.state = module.params['state']
        self.template_data = list()
        self.device_version = None
        self.module = module


    def validate(self):
        if (self.credentials['certificate'] is not None and self.credentials['certificate_key'] is None) or (self.credentials['certificate_key'] is not None and self.credentials['certificate'] is None):
            self.module.fail_json(msg="Specify the certificate along with the certificate_key for the VSD API")

        if (self.template_name is None and self.variables is not None and len(self.variables)>0 ):
            self.module.fail_json(changed=False,msg="Specify a template_name to apply config")

        if (self.template_name is not None and self.variables is None):
            self.module.fail_json(changed=False,msg="Specify a list of dictionaries of variable/values sets to apply to template")

        if self.spec_path is None:
            self.module.fail_json(changed=False,msg="Specify the path to the folder containing the specification of API for VSD")

        if self.template_path is None:
            self.module.fail_json(changed=False,msg="Specify The path to the folder containing the templates")

    def run(self):

        # set logging to Stream IO
        self.set_logging()

        # read and load the template
        self.load_templates_to_store()

        # read and load the specs
        self.load_specs_to_write()

        # set the writer session parameters
        self.set_vsd_writer_session()

        # read and load the user data
        self.parse_user_data()

        # parse extra configs
        self.parse_extra_configs()

        # apply the state
        self.apply_state()

    def set_logging(self):

        OUTPUT_LEVEL_NUM = logging.ERROR + 5
        logging.addLevelName(OUTPUT_LEVEL_NUM, "OUTPUT")
        def output(self, msg, *args, **kwargs):
            if self.isEnabledFor(OUTPUT_LEVEL_NUM):
                self._log(OUTPUT_LEVEL_NUM, msg, args, **kwargs)

        logging.Logger.output = output
        self.logger = logging.getLogger("metroae_config")
        log_formatter = logging.Formatter("%(levelname)-6s: %(message)s")
        self.log_capture_string =  io.StringIO()
        self.logger.setLevel(logging.DEBUG)
        debug_handler = CustomLogHandler(self.log_capture_string)
        debug_handler.setFormatter(log_formatter)
        self.logger.addHandler(debug_handler)

    def load_templates_to_store(self):
        self.store = TemplateStore(LEVISTATE_VERSION)
        for path in self.template_path:
            try:
                self.store.read_templates(path)
            except TemplateParseError as e:
                self.module.fail_json(msg=str(e))
            except Exception as e:
                self.module.fail_json(msg=str(e))

    def load_specs_to_write(self):
        self.writer = VsdWriter()
        self.writer.set_logger(self.logger)
        for path in self.spec_path:
            try:
                self.writer.read_api_specifications(path)
            except InvalidSpecification as e:
                self.module.fail_json(msg=str(e))
            except Exception as e:
                self.module.fail_json(msg=str(e))


    def set_vsd_writer_session(self):
        self.writer.set_session_params(self.credentials['url'],
                                username=self.credentials['username'],
                                password=self.credentials['password'],
                                enterprise=self.credentials['enterprise'],
                                certificate=(self.credentials['certificate'],
                                            self.credentials['certificate_key']
                                            )
                                )
        if self.device_version is None:
            try:
                self.device_version = self.writer.get_version()
            except Exception as e:
                self.module.fail_json(msg=str(e))

    def parse_user_data(self):
        parser = UserDataParser()
        if not (self.user_data_path is None or len(self.user_data_path) == 0):
            try:
                for path in self.user_data_path:
                    parser.read_data(path)
                self.template_data = parser.get_template_name_data_pairs()
            except LevistateError as e:
                self.module.fail_json(msg=str(e))
            except Exception as e:
                self.module.fail_json(msg=str(e))

    def parse_extra_configs(self):
        if self.template_name is not None and self.variables is not None:
                for data in self.variables:
                    self.template_data.append((self.template_name, data))

    def apply_state(self):
        config = Configuration(self.store)
        config.set_software_version(self.get_software_type(),
                                    self.get_software_version())
        config.set_logger(self.logger)
        try:
            for data in self.template_data:
                template_name = data[0]
                template_data = data[1]
                config.add_template_data(template_name, **template_data)

            self.writer.set_validate_only(False)
            if self.state == STATE_ABSENT:
                config.revert(self.writer)           # Revert the configuration
            else:
                config.apply(self.writer)           # update/apply the configuration

        except Exception as e:
            self.module.fail_json(msg=str(e))

        self.module.exit_json(changed=True, message="All configurations applied to the VSD")

    def get_software_type(self):
        if self.device_version is not None:
            return self.device_version['software_type']
        else:
            return None

    def get_software_version(self):
        if self.device_version is not None:
            return self.device_version['software_version']
        else:
            return None


def main():
    arg_spec = dict(
                spec_path=dict(required=True, type='list'),
                template_path=dict(required=True, type='list'),
                user_data_path=dict(required=False, type='list'),
                template_name=dict(required=False,type='str'),
                variables=dict(required=False,type='list'),
                credentials=dict(required=True,
                                type='dict',
                                no_log=True,
                                options=dict( username=dict(type='str',required=True),
                                            password=dict(type='str',required=True),
                                            enterprise=dict(type='str',required=True),
                                            url=dict(type='str',required=True),
                                            certificate=dict(type='str',required=False),
                                            certificate_key=dict(type='str',required=False)
                                )
                            ),
                state=dict(required=True,type='str',choices=['absent', 'present'])
                )
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=False,
                               required_one_of=[['user_data_path','template_name']], required_together=[['template_name','variables']])
    metroae = MetroaeConfig(module)
    metroae.validate()
    metroae.run()
#    result['changed'] = True
    module.exit_json(msg="Fatal exception has occured")

if __name__ == '__main__':
    main()

