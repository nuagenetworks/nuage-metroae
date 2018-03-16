#!/usr/bin/python

from jsonschema import validate, ValidationError
import yaml

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: validate_against_schema
short_description: Ensures that a YAML file matches a schema
options:
  path:
    description:
      - The file path to the file that needs to be checked
    required:True
  schema:
    description:
      - The file path to the schema to check against
    required:True

'''

EXAMPLES = '''
- validate_against_schema:
    path: ./deployments/default/vsds.yml
    schema: ./schemas/vsds.json
'''


def validate_against_schema(path, schema):
    with open(schema, 'r') as file:
        try:
            parsed_schema = yaml.safe_load(file.read())
        except Exception as e:
            msg = "Could not load schema %s: %s" % (schema, str(e))
            print msg
            module.fail_json(msg=msg)

    with open(path, 'r') as file:
        try:
            parsed_yaml = yaml.safe_load(file.read())
        except Exception as e:
            msg = "Could not load yaml file %s: %s" % (path, str(e))
            print msg
            module.fail_json(msg=msg)

    if parsed_yaml is None:
        parsed_yaml = dict()
    try:
        validate(parsed_yaml, parsed_schema)
        module.exit_json(changed=False)
    except ValidationError as e:
        msg = "Invalid data in %s: %s" % (path, e.message)
        print msg
        module.fail_json(msg=msg)


arg_spec = dict(
    path=dict(
        required=True,
        type='str'),
    schema=dict(
        required=True,
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    schema = module.params['schema']
    validate_against_schema(path, schema)


if __name__ == '__main__':
    main()
