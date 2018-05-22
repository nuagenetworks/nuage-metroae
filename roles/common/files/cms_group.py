from vspk.v4_0 import NUEnterprise, NUUser, NUVSDSession
import yaml
import sys
import argparse


def add_cspto_cms(session):
    cspenterprise = NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    print lst_users
    csprootuser = NUUser(id=session.me.id)
    csprootuser.fetch()
    # Add csproot user to CMS group
    csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                  'CMS Group'")
    csprootgroup.assign([csprootuser, csprootuser], NUUser)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Set path to playbook directory.")
    parser.add_argument("vsd_ip_addr", type=str,
                        help="IP address of VSD machine")
    args = parser.parse_args()

    # Get VSD related parameters
    try:
        playbook_dir = args.playbook_dir.strip('playbooks')
        with open(playbook_dir + 'group_vars/all', 'r') as fh:
            vsd_params = yaml.load(fh)
    except Exception as e:
        print("ERROR: Failure reading file: %s" % e)

    # Create a session as csp user
    try:
        vsd_params['vsd_auth']['api_url'] = 'https://' +\
            args.vsd_ip_addr + ':8443'
        session = NUVSDSession(**vsd_params['vsd_auth'])
        session.start()
        csproot = session.user
    except Exception as e:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)
    add_cspto_cms(session)
