#!/usr/bin/python

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
    required:False
    default: './build_vars.yml'

'''

EXAMPLES = '''
- yaml_checker: path=./roles/nuage-predeploy/tasks/main.yml
'''


def check_yaml(filepath):
    fil = open(filepath, 'r')
    try:
        yaml.load(fil, yaml.SafeLoader)
        module.exit_json(changed=False)
    except yaml.YAMLError as exc:
        print("Error while parsing YAML file:")
        if hasattr(exc, 'problem_mark'):
            if exc.context is not None:
                msg1 = "YAML Syntax Error" + str(exc.problem_mark) + ":" + str(
                    exc.problem) + str(exc.context) + "--- Please correct data and retry."
                module.fail_json(msg=msg1)
            else:
                msg1 = "YAML Syntax Error" + \
                    str(exc.problem_mark) + " : " + str(exc.problem) + "--- Please correct data and retry."
                module.fail_json(msg=msg1)
        else:
            module.fail_json(
                msg="Something went wrong while parsing yaml file")


arg_spec = dict(
    path=dict(
        required=False,
        default='./build_vars.yml',
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    check_yaml(path)


if __name__ == '__main__':
    main()
