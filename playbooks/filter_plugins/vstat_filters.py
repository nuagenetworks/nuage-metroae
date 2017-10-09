#!/usr/bin/python

import json
import re

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


def snapshot_list_indices_to_json(string):
    ''' Given a string representation of the output of
    "vsdelasticctl.py -a <ip> list_indices" or
    "vsd_elasticctl.py -a <ip> show_snapshot <snapshot> -r <repo>"
    as a string,
    return a JSON representation of a subset of the data in that output.
    A sample of the output after running script
    {
      "indices": ['nuage_acl-2017-05-11', 'nuage_acl-2017-05-12']
    }
    '''
    if string:
        lst_indices = re.findall(r'(\w+_\w+-.*)', string)
        indices = {'indices': lst_indices}
    else:
        indices = {'indices': []}
    return json.dumps(indices)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'snapshot_list_indices_to_json': snapshot_list_indices_to_json,
        }
