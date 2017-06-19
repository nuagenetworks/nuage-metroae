#!/usr/bin/python
import yaml
from ansible.module_utils.basic import AnsibleModule
from yaml.constructor import ConstructorError

DOCUMENTATION = '''

---
module: build_vars_checker
short_description: Ensures that build_vars.yml has no duplicate keys and that HA deployments have three VSDs defined
options:
   path:
     description:
         - The name(along with path) of the file to be checked
     required: False
     default: './build_vars.yml'
'''

EXAMPLES = '''
- build_vars_checker: path=./build_vars.yml
'''

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def no_duplicates_constructor(loader, node, deep=False):
    """Check for duplicate keys."""
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        value = loader.construct_object(value_node, deep=deep)
        if key in mapping:
            module.fail_json(msg="Duplicate Variable Found - %s" % key)

        mapping[key] = value

    return loader.construct_mapping(node, deep)


yaml.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    no_duplicates_constructor)


def check_buildvars(filepath):
    fil = open('build_vars.yml')
    config = yaml.load(fil)
    if config['vsd_sa_or_ha'] == 'ha':
        if len(config['myvsds']) != 3:
            module.fail_json(
                msg="FAIL: HA Deployments require 3 VSDs to be defined")
        else:
            module.exit_json(changed=False)
    elif config['vsd_sa_or_ha'] == 'sa':
        module.exit_json(changed=False)
    else:
        module.exit_json(msg="FAIL: vsd_sa_or_ha should be one of sa or ha")


arg_spec = dict(
    path=dict(
        required=False,
        default='./build_vars.yml',
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    check_buildvars(path)


if __name__ == '__main__':
    main()
