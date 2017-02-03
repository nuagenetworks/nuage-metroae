from vspk.v4_0 import NULicense, NUEnterprise, NUUser, NUVSDSession
import yaml
import sys
import argparse


def install_license(csp_user, vsd_license):
    csproot = csp_user
    # Clear any existing license
    installed_licenses = csproot.licenses.get()
    for lic in installed_licenses:
        lic.delete()

    # Push the license
    test_license = NULicense(license=vsd_license)
    csproot.create_child(test_license)


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
    args = parser.parse_args()

    # Get ZFB related parameters
    try:
        with open(args.playbook_dir + '/zfb.yml', 'r') as fh:
            zfb_params = yaml.load(fh)
    except Exception as e:
        print("ERROR: Failure reading file: %s" % e)

    # Get VSD license
    vsd_license = ""
    try:
        with open(zfb_params['vsd_license_file'], 'r') as lf:
            vsd_license = lf.read()
    except Exception as e:
        print("ERROR: Failure reading file: %s" % e)

    # Create a session as csp user
    try:
        session = NUVSDSession(**zfb_params['csp'])
        session.start()
        csproot = session.user
    except:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)
    install_license(csproot, vsd_license)
    add_cspto_cms(session)
