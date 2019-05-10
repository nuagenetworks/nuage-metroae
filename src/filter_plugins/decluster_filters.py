#!/usr/bin/env python

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


def ejabberd_list_p1db_to_json(string):
    ''' Given a string representation of the output of
    "/opt/ejabberd/bin/ejabberdctl list_p1db" as a string,
    return a JSON representation of a subset of the data in that output.
    A sample of the output after running script
    {
      "p1db_users": []
    }
    {
      "p1db_users": ["'ejabberd@vsd1.example.com'","'ejabberd@vsd3.example.com'"]
    }
    '''
    if string:
        lst_p1db = string.split('\n')
        p1db = {'p1db_users': lst_p1db}
    else:
        p1db = {'p1db_users': []}
    return json.dumps(p1db)


def ejabberd_list_cluster_to_json(string):
    ''' Given a string representation of the output of
    "/opt/ejabberd/bin/ejabberdctl list_cluster" as a string,
    return a JSON representation of a subset of the data in that output.
    A sample of the output after running script
    {
      "cluster_users": ["'ejabberd@vsd2.example.com'"]
    }
    '''
    if not string:
        return json.dumps({'cluster_users': []})
    string = string.replace("'", "")
    lst_cluster_users = string.split('\n')
    cluster_users = {'cluster_users': lst_cluster_users}
    return json.dumps(cluster_users)


def ejabberd_list_clients_to_json(string):
    ''' Given a string representation of the output of
    "/opt/ejabberd/bin/ejabberdctl connected_users" as a string,
    return a JSON representation of a subset of the data in that output.
    A sample of the output after running script
    {
      "connected_clients": ["push@xmpp.example.com/vsd1",
                            "cna@xmpp.example.com/vsd1",
                            "keyserver@xmpp.example.com/vsd1"
                           ]
    }
    '''
    if not string:
        return json.dumps({'connected_clients': []})
    lst_clients = string.split('\n')
    clients = {'connected_clients': lst_clients}
    return json.dumps(clients)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'ejabberd_p1db_to_json': ejabberd_list_p1db_to_json,
            'ejabberd_cluster_to_json': ejabberd_list_cluster_to_json,
            'ejabberd_clients_to_json': ejabberd_list_clients_to_json,
        }
