from vspk.v4_0 import NUVSDSession
import sys
import yaml
import argparse
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


def update_gw_purge_timer(csproot):
    try:
        sys_config = csproot.system_configs.get_first()
        sys_config.ad_gateway_purge_time = int(sys_params['gw_purge_time'])
        sys_config.save()
        print('Updated gateway purge timer')
        return (True)
    except:
        print('ERROR: Could not update gateway purge timer')
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Path to playbook directory.")
    args = parser.parse_args()

    # Get system config related parameters
    try:
        params_path = '/roles/db-backup/vars/main.yml'
        with open(args.playbook_dir + params_path, 'r') as fh:
            sys_params = yaml.load(fh)
    except Exception as e:
        print("ERROR: Could not locate file: %s" % e)

    # Create a session as csp user
    try:
        session = NUVSDSession(**sys_params['csp'])
        session.start()
        csproot = session.user
    except:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)

    # Update gw purge timer
    update_gw_purge_timer(csproot)
