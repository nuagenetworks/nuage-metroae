#!/usr/bin/env python

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


def vault_constructor(loader, node):
    return node.value


def validate_against_schema(module, path, schema):
    with open(schema, 'r') as file:
        try:
            parsed_schema = yaml.safe_load(file.read())
        except Exception as e:
            msg = "Could not load schema %s: %s" % (schema, str(e))
            print(msg)
            module.fail_json(msg=msg)
            return

    with open(path, 'r') as file:
        try:
            yaml.add_constructor('!vault', vault_constructor)
            parsed_yaml = yaml.load(file.read())
        except Exception as e:
            msg = "Could not load yaml file %s: %s" % (path, str(e))
            print(msg)
            module.fail_json(msg=msg)
            return

    if parsed_yaml is None:
        parsed_yaml = dict()
    try:
        validate(parsed_yaml, parsed_schema)
        module.exit_json(changed=False)
    except ValidationError as e:

        field = ""
        if "title" in e.schema:
            field = " for " + e.schema["title"]
        msg = "Invalid data in %s%s: %s" % (path, field, e.message)
        print(msg)
        module.fail_json(msg=msg)
        return


def main():
    arg_spec = dict(
        path=dict(
            required=True,
            type='str'),
        schema=dict(
            required=True,
            type='str'))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    path = module.params['path']
    schema = module.params['schema']
    validate_against_schema(module, path, schema)


if __name__ == '__main__':
    main()
