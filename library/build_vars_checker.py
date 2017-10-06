#!/usr/bin/python
import yaml
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: build_vars_checker
short_description: Ensures that build_vars.yml has no duplicate keys and that HA deployments have three VSDs defined
options:
   path:
     description:
         - The name(along with path) of the file to be checked
     required: True
'''

EXAMPLES = '''
- build_vars_checker: path=./build_vars.yml
'''


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
    fil = open(filepath)
    config = yaml.load(fil)
    if 'vsd_sa_or_ha' in config:
        if config['vsd_sa_or_ha'] == 'ha':
            if len(config['myvsds']) != 3:
                module.fail_json(
                    msg="FAIL: HA Deployments require 3 VSDs to be defined")
        elif config['vsd_sa_or_ha'] != 'sa':
            module.fail_json(msg="FAIL: vsd_sa_or_ha should be one of sa or ha")
    hostnames = []
    for key in config:
        if type(config[key]) is list:
            for dic in config[key]:
                if 'hostname' in dic:
                    hostnames.append(dic['hostname'])
    hostnames_set = set([x for x in hostnames if hostnames.count(x) > 1])
    if len(hostnames_set) != 0:
        module.fail_json(msg=("Error : The following hostnames are not unique - " + ','.join(hostnames_set)))
    else:
        module.exit_json(changed=False)

arg_spec = dict(
    path=dict(
        required=False,
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    check_buildvars(path)


if __name__ == '__main__':
    main()
