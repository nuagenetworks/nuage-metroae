#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: nuage_append
short_description: Make sure filename exists and append information to a report file
options:
  filename:
    description:
      - The name of the file to append to
    required: true
    default: null
  text:
    description:
      - The text to append to the file
    required: true
    default: null
'''

EXAMPLES = '''
- nuage_append: filename=/home/caso/report.json text="{\"taxes owed\": \"0.00\"}"
'''


def main():
    arg_spec = dict(
        filename=dict(required=True),
        text=dict(required=True)
    )

    module = AnsibleModule(argument_spec=arg_spec)

    filename = module.params['filename']
    text = module.params['text']

    with open(filename, "a") as myfile:
        myfile.write(text)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
