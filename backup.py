#!/usr/bin/env python

import importlib
import logging

VSPK = None

DOCUMENTATION = '''
---
module: change_csproot_creds
short_description: Change credentials for csproot user
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
  new_pass:
    description:
      - New password for the csproot user
    required: true
    default: ""
'''

EXAMPLES = '''
# Check if new license are required after the upgrade
- check_vsd_license_validity:
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://10.0.0.10:8443
    new_pass: newpass
'''


def get_vsd_session(vsd_auth):
    # Format api version
    version = 'v5_0'
    try:
        global VSPK
        VSPK = importlib.import_module('vspk.{0:s}'.format(version))
    except ImportError:
            print "No VSPK"
    try:
        session = VSPK.NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
        return csproot
    except Exception as e:
        print "I failed"+ e


arg_spec = dict(vsd_auth=dict(required=True, type='dict'),
                new_pass=dict(required=True, type='str'))


def main():

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    bambou_logger = logging.getLogger("bambou")
    bambou_logger.setLevel(logging.DEBUG)
    bambou_logger.addHandler(fh)
    vsd_auth = {
          "username": "csproot",
          "password": "csproot",
          "enterprise": "csp",
          "api_url": "https://vsd1.example.met:8443"
          }
    new_pass = "abcdef"

    try:
        csproot = get_vsd_session(vsd_auth)
        print str(csproot.user_name)
        csproot.password = new_pass
        csproot.save()
        print str(csproot.password)
    except Exception as e:
        print "failure to save password"+ str(e)
        return

    print "success"


# Run the main

if __name__ == '__main__':
    main()
