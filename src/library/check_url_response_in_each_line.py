#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import time
import requests

DOCUMENTATION = '''
---
module: check_url_response_in_each_line
short_description: Perfrom a GET request on the url and check its response for search string in each line
options:
  url:
    description:
      - The url to perform GET on
    required: true
    default: null
  search_string:
    description:
      - String  that needs to be looked up in each line
  timeout_seconds:
    description:
      - time timeout_seconds to keep trying
    required: true
    default: null
  test_interval_seconds:
    description:
      - test_interval_seconds of polling
    required: true
    default: null
'''

def main():
    arg_spec = dict(
        url=dict(required=True, type='path'),
        search_string=dict(required=True),
        timeout_seconds=dict(required=True, type='int'),
        test_interval_seconds=dict(required=True, type='int')
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    timeout_seconds = module.params['timeout_seconds']
    test_interval_seconds = module.params['test_interval_seconds']
    search_string = module.params['search_string']
    found_all_search_strings = False
    time_elapsed = 0
    response_text = ""

    while not found_all_search_strings and time_elapsed < timeout_seconds:
        found_all_search_strings = True
        resp = requests.get(module.params['url'])
        response_text = resp.text
        for line in response_text.splitlines():
            if line.find(search_string) == -1:
                found_all_search_strings = False

            if not found_all_search_strings:
                break

        time.sleep(test_interval_seconds)
        time_elapsed = time_elapsed + test_interval_seconds

    if found_all_search_strings:
        module.exit_json(changed=True, response=response_text)
    else:
        module.fail_json(msg="Did not find the search string %s from response %s within %i seconds" % (search_string, response_text, timeout_seconds))
        # Run the main

main()
