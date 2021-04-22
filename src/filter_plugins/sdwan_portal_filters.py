#!/usr/bin/env/python

import re
import json

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

def string_name_value_helper(name, delimiter, string):
    ''' Matches "name <delimiter> <text_value>" in the string and returns <text_value>
    If no match, returns "None"
    '''
    VALUE_RE = "\s*" + "\\"+delimiter + "\s*(\S+)\s+"
    scratch = re.search(name + VALUE_RE, string)
    if scratch:
        return scratch.group(1)
    else:
        return "None"

def cluster_bootstrap_status_to_json(string):
    WSREP_CLUSTER_STATUS = "wsrep_cluster_status"
    WSREP_CONNECTED = "wsrep_connected"
    WSREP_EVS_STATE = "wsrep_evs_state"
    WSREP_LOCAL_STATE_COMMENT = "wsrep_local_state_comment"

    dict = {}

    dict[WSREP_CLUSTER_STATUS] = string_name_value_helper(WSREP_CLUSTER_STATUS, "|", string) + ","
    dict[WSREP_CONNECTED] = string_name_value_helper(WSREP_CONNECTED, "|", string) + ","
    dict[WSREP_EVS_STATE] = string_name_value_helper(WSREP_EVS_STATE, "|", string) + ","
    dict[WSREP_LOCAL_STATE_COMMENT] = string_name_value_helper(WSREP_LOCAL_STATE_COMMENT, "|", string) + ","

    return json.dumps(dict)

class FilterModule(object):

    def filters(self):
        return {
            'cluster_bootstrap_status_to_json': cluster_bootstrap_status_to_json
        }
