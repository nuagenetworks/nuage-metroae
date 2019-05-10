#!/usr/bin/env python

import os
import time

from ansible.plugins.callback import CallbackBase


#    Copyright 2017 Nokia
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


class CallbackModule(CallbackBase):
    """
    logs select playbook results in ./failure_report.log
    """
    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'report_failures'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT = "%b %d %Y %H:%M:%S"

    DESTINATION_FILE = "./failure_report.log"

    def __init__(self):

        super(CallbackModule, self).__init__()

        if os.path.exists(self.DESTINATION_FILE):
            os.remove(self.DESTINATION_FILE)

    def log_failed(self, host, category, res):
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        if type(res) == dict and 'msg' in res.keys():
            with open(self.DESTINATION_FILE, "ab") as fd:
                fd.write(u'{0}: {1}: {2}: {3}\n'.format(now, category, host, res['msg']))
        else:
            with open(self.DESTINATION_FILE, "ab") as fd:
                fd.write(u'{0}: {1}: {2}: {3}\n'.format(now, category, host, "Unknown failure"))

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.log_failed(host, 'FAILED', res)

    def runner_on_ok(self, host, res):
        pass

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        self.log_failed(host, 'UNREACHABLE', res)

    def runner_on_async_failed(self, host, res, jid):
        self.log_failed(host, 'ASYNC_FAILED', res)

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass
