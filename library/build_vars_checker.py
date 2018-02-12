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
    if 'myvsds' in config:
        num_vsds = len(config['myvsds'])
        if (num_vsds != 3) or (num_vsds != 1):
            module.fail_json(
                msg="FAIL: You must define exactly 1 or exactly 3 vsds")
    if 'myvscs' in config:
        num_vscs = len(config['myvscs'])
        if (num_vscs != 3) or (num_vscs != 1):
            module.fail_json(
                msg="FAIL: You must define exactly 1 or exactly 2 vscs")
    if 'myvstats' in config:
        num_vstats = len(config['myvstats'])
        if (num_vstats != 3) or (num_vstats != 1):
            module.fail_json(
                msg="FAIL: You must define exactly 1 or exactly 3 vstats")
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
