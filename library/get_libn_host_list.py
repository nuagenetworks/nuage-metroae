#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import yaml

DOCUMENTATION = '''

---
module: get_libn_host_list
short_description: Returns list of hosts on which Libnetwork is to be installed
options:
   path:
     description:
         - Path to the file that has the VRS information.
     required: True
'''

EXAMPLES = '''
- get_libn_host_list: path=./build_vars.yml
'''


def libn_check(filepath):
    try:
        with open(filepath) as fil:
            config = yaml.load(fil)
    except IOError as details:
        module.fail_json(msg="Error processing YAML file: %s" % details)

    vrs_list = []
    if 'myvrss' not in config:
        return vrs_list

    for item in config['myvrss']:
        if 'libnetwork_install' in item and item['libnetwork_install']:
            if 'vrs_ip_list' not in item:
                module.fail_json(msg="Build variables specify libnetwork_install without VRS IP addressess")
            for ip in item['vrs_ip_list']:
                vrs_list.append(ip)
    return vrs_list


arg_spec = dict(
    path=dict(
        required=False,
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    result = libn_check(path)
    module.exit_json(meta=result)


if __name__ == '__main__':
    main()
