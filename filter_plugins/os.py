#!/usr/bin/python

import re
import json
from datetime import datetime, timedelta


# Copyright 2017 Nokia
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


def os_env_dict(os_env_string):
    ''' Given a string representation of the output of "cat os_env_file",
    return a dictionary of env values for use with ansible commands. Assumes
    each line of the env file is of the form:

    export NAME=VALUE

    For example:

    export OS_USERNAME=admin
    export OS_AUTH_URL="http://10.100.100.20:35357/v3"
    '''
    PAIR_RE = "export\s+(?P<name>\w+)=(?P<value>\S+)"
    dict = {}
    pairs = re.finditer(PAIR_RE, os_env_string)
    for pair in pairs:
        dict[pair.group('name')] = pair.group('value').strip('"')
    return dict


def openstack_stack_list_to_json(string, older_than_hours=0, use_utc=True):
    ''' Given a string representation of the output of "openstack stack list"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "openstack stack list",
      "Older Than Hours": "3",
      "Current time": "2017-05-01T20:56:40",
      "Stack Count Total": "2",
      "Stack Count Filtered": "2",
      "Stacks": [
        {
          "ID": "dbfd3ccf-3147-4515-99c1-e559d0a35dec",
          "Name": "jen-slave-u16-395",
          "Status": "CREATE_COMPLETE",
          "CreationTime": "2017-05-01T20:56:40",
          "UpdatedTime": "None"
        },
        {
          "ID": "dbfd3ccf-3147-4515-99c1-e559d0a35737",
          "Name": "jen-slave-u14-477",
          "Status": "CREATE_COMPLETE",
          "CreationTime": "2017-05-01T22:56:40",
          "UpdatedTime": "None"
        }
      ]
    }
    '''
    STACK_RE = ("[|]\s+(?P<id>\S+)\s+[|]\s+(?P<stack_name>\S+)\s+[|]\s+(?P<stack_status>\S+)\s+[|]\s+(?P<creation_time>\S+)\s+[|]\s+(?P<updated_time>\S+)\s+[|]\n")
    dict = {}
    stack_list = []
    stack_count_total = 0
    dict["Command"] = "openstack stack list"
    dict["Older Than Hours"] = older_than_hours
    current_time = datetime.utcnow() if use_utc else datetime.now()
    dict["Current Time"] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    stacks = re.finditer(STACK_RE, string)
    for stack in stacks:
        stack_count_total += 1
        if older_than_helper(stack.group('creation_time'), older_than_hours, current_time):
            stack_dict = {}
            stack_dict["ID"] = stack.group('id')
            stack_dict["Name"] = stack.group('stack_name')
            stack_dict["Status"] = stack.group('stack_status')
            stack_dict["CreationTime"] = stack.group('creation_time')
            stack_dict["UpdatedTime"] = stack.group('updated_time')
            stack_list.append(stack_dict)
    dict["Stacks"] = stack_list
    dict["Stack Count Total"] = stack_count_total
    dict["Stack Count Filtered"] = len(stack_list)
    return json.dumps(dict)


def older_than_helper(stack_time, older_than_hours, current_time):
    '''
    Given a stack time of the form "2017-05-01T20:56:40" and a number of delta hours
    to check against, return True if the time is at least older_than_hours old. Return
    False if the stack_time is less than older_than_hours old.
    '''
    target_time = current_time - timedelta(hours=older_than_hours)
    stack_time_parsed = datetime.strptime(stack_time, '%Y-%m-%dT%H:%M:%S')
    if stack_time_parsed < target_time:
        return True
    return False


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'os_env_dict': os_env_dict,
            'openstack_stack_list_to_json': openstack_stack_list_to_json
        }
