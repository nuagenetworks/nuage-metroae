#!/usr/bin/env python

import yaml
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: yaml_checker
short_description: Ensures that a YAML file's syntax is correct.
options:
  path:
    description:
      - The file path to the file that needs to be checked
    required:True

'''

EXAMPLES = '''
- yaml_checker: path=./roles/vsd-predeploy/tasks/main.yml
'''


def no_duplicates_constructor(loader, node, deep=False):
    """Check for duplicate keys."""
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        value = loader.construct_object(value_node, deep=deep)
        if key in mapping:
            raise KeyError("Duplicate Variable Found - %s" % key)

        mapping[key] = value

    return loader.construct_mapping(node, deep)


def vault_constructor(loader, node):
    return node.value


def check_yaml(filepath):
    with open(filepath, 'r') as fil:
        yaml.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            no_duplicates_constructor)
        yaml.add_constructor(u'!vault', vault_constructor)
        yaml.load(fil, Loader=yaml.Loader)


def main():
    arg_spec = dict(
        path=dict(
            required=True,
            type='str'))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    path = module.params['path']

    try:
        check_yaml(path)
        module.exit_json(changed=False)
    except KeyError as ke:
        module.fail_json(msg=str(ke))
        return
    except yaml.YAMLError as exc:
        print("Error while parsing YAML file:")
        if hasattr(exc, 'problem_mark'):
            if exc.context is not None:
                msg1 = "".join(["YAML Syntax Error",
                                str(exc.problem_mark), ": ",
                                str(exc.problem),
                                str(exc.context),
                                "--- Please correct data and retry."])
            else:
                msg1 = "".join(["YAML Syntax Error",
                                str(exc.problem_mark), " : ",
                                str(exc.problem),
                                "--- Please correct data and retry."])
            module.fail_json(msg=msg1)
            return
        else:
            module.fail_json(
                msg="Something went wrong while parsing yaml file")
            return


if __name__ == '__main__':
    main()
