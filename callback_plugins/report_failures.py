# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import time
import json

from ansible.module_utils._text import to_bytes
from ansible.plugins.callback import CallbackBase


# NOTE: in Ansible 1.2 or later general logging is available without
# this plugin, just set ANSIBLE_LOG_PATH as an environment variable
# or log_path in the DEFAULTS section of your ansible configuration
# file.  This callback is an example of per hosts logging for those
# that want it.


class CallbackModule(CallbackBase):
    """
    logs select playbook results in ./failure_report.log
    """
    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'report_failures'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT="%b %d %Y %H:%M:%S"

    DESTINATION_FILE="./failure_report.log"

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

