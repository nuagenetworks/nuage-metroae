#!/usr/bin/python

from vspk.v4_0 import NULicense, NUEnterprise, NUUser, NUNSPortTemplate
from vspk.v4_0 import NUInfrastructureGatewayProfile, NUNSGatewayTemplate
from vspk.v4_0 import NUInfrastructureVscProfile, NUVLANTemplate, NUJob
from vspk.v4_0 import NUNSGateway, NUVSDSession, NUUplinkConnection
import subprocess
import sys
from time import sleep

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: create_zfb_profile
short_description: Creates a zero-factor bootstrap profile for NSGvs
options:
  nsgv_path:
    description:
      - Set path to NSGV ISO output directory.
    required:True
  fact_name:
    description:
      - Name of fact variable to state if NSGv is already configured
    required:True
  vsd_auth:
    description:
      - Authorization parameters dictionary for VSD API
    required:True
  zfb_constants:
    description:
      - Constants required for ZFB
    required:True
  zfb_params:
    description:
      - Parameters required for ZFB
    required:True

'''

EXAMPLES = '''
- create_zfb_profile:
    nsgv_path: /tmp/ansible.1234
    fact_name: nsgv_already_configured,
    vsd_auth: "{{ vsd_auth }}"
    zfb_constants: "{{ zfb_constants }}"
    zfb_params: "{{ zfb_params }}"
'''


def install_license(csp_user, vsd_license):
    csproot = csp_user

    # Push the license
    test_license = NULicense(license=vsd_license)
    csproot.create_child(test_license)


def is_license_already_installed(csp_user, vsd_license):
    csproot = csp_user
    license_unique_id = get_license_unique_id(vsd_license)

    installed_licenses = csproot.licenses.get()
    for lic in installed_licenses:
        if lic.unique_license_identifier == license_unique_id:
            return True

    return False


def get_license_unique_id(vsd_license):
    stripped = vsd_license.strip()
    return unicode(stripped[0:16] + stripped[-16:])


def create_proxy_user(session):
    zfb_params = module.params['zfb_params']
    zfb_constants = module.params['zfb_constants']

    # Create proxy user if not present
    cspenterprise = NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if 'proxy' not in lst_users:
        proxy_user = NUUser(first_name=zfb_params['user_data']['firstName'],
                            last_name=zfb_params['user_data']['lastName'],
                            user_name=zfb_constants['proxy_user'],
                            email=zfb_params['user_data']['email'],
                            password=zfb_params['user_data']['password'])
        cspenterprise.create_child(proxy_user)
        csprootuser = NUUser(id=session.me.id)
        csprootuser.fetch()
        # Add proxy user to root group
        csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                      'Root Group'")
        csprootgroup.assign([proxy_user, csprootuser], NUUser)


def get_nsg_gateway_template(csp_user):
    zfb_params = module.params['zfb_params']

    csproot = csp_user
    vns_nsg = zfb_params['vns_nsg']
    temp_name = vns_nsg.get('nsg_template_name')
    nsg_temp = csproot.ns_gateway_templates.get_first(
        "name is '%s'" % temp_name)
    infra_profile = csproot.infrastructure_gateway_profiles.get_first(
        "name is '%s'" % vns_nsg.get('name'))
    if (nsg_temp is None or
            infra_profile is None or
            nsg_temp.infrastructure_profile_id != infra_profile.id):
        nsg_temp = None
    return nsg_temp


def create_nsg_gateway_template(csp_user):
    zfb_params = module.params['zfb_params']
    zfb_constants = module.params['zfb_constants']

    csproot = csp_user
    vns_nsg = zfb_params['vns_nsg']
    temp_name = vns_nsg.get('nsg_template_name')
    nsg_temp = NUNSGatewayTemplate(name=temp_name)

    # Fetch current infra profiles
    infra_profiles = csproot.infrastructure_gateway_profiles.get()
    lst_infra_names = [infra.name for infra in infra_profiles]
    if vns_nsg['name'] not in lst_infra_names:
        # Create infra profile
        zfb_params['vns_nsg']['useTwoFactor'] = zfb_constants['useTwoFactor']
        zfb_params['vns_nsg']['upgradeAction'] = zfb_constants['upgradeAction']
        nsg_infra = NUInfrastructureGatewayProfile(data=vns_nsg)
        csproot.create_child(nsg_infra)
        # Attach the infra profile to NSG template
        vns_infra_profile = csproot.infrastructure_gateway_profiles.\
            get_first(filter="name == '%s'" % vns_nsg['name'])
        infra_id = vns_infra_profile.id
        nsg_temp.infrastructure_profile_id = infra_id
        csproot.create_child(nsg_temp)
    return nsg_temp


def create_vsc_template(csp_user):
    zfb_params = module.params['zfb_params']

    csproot = csp_user
    vns_vsc = zfb_params['vns_vsc']
    # Fetch current infra vsc profile
    vsc_temp = NUInfrastructureVscProfile(data=vns_vsc)
    infra_vsc_profiles = csproot.infrastructure_vsc_profiles.get()
    lst_infra_vsc = [infra.name for infra in infra_vsc_profiles]
    if vns_vsc['name'] not in lst_infra_vsc:
        # Create infra vsc profile
        csproot.create_child(vsc_temp)
    return vsc_temp


def create_nsgv_ports(nsg_temp, vsc_temp):
    zfb_params = module.params['zfb_params']
    zfb_constants = module.params['zfb_constants']

    # Create network port
    network_port = zfb_params['nsg_ports']['network_port']
    access_port = zfb_params['nsg_ports']['access_port']
    port_info = nsg_temp.ns_port_templates.get()
    lst_port_name = [port.name for port in port_info]
    if network_port['name'] not in lst_port_name:
        network_port['portType'] = zfb_constants['network_port_type']
        port_temp = NUNSPortTemplate(data=network_port)
        nsg_temp.create_child(port_temp)
        # Attach vlan0 and vsc profile
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = '0'
        vlan_temp.associated_vsc_profile_id = vsc_temp.id
        port_temp.create_child(vlan_temp)

        uplink = NUUplinkConnection()
        uplink.mode = "Dynamic"
        uplink.role = "PRIMARY"
        vlan_temp.create_child(uplink)

    # Create access port
    if access_port['name'] not in lst_port_name:
        vlan_id = access_port.pop('vlan_value')
        access_port['portType'] = zfb_constants['access_port_type']
        port_temp = NUNSPortTemplate(data=access_port)
        nsg_temp.create_child(port_temp)
        # Attach vlan
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = vlan_id
        port_temp.create_child(vlan_temp)


def create_nsg_device(csp_user, nsg_temp):
    zfb_params = module.params['zfb_params']

    csproot = csp_user
    organization = zfb_params['organization']
    # Create an ORG/Enterprise
    metro_org = NUEnterprise(name=organization['name'])
    csproot.create_child(metro_org)

    # Create NSG device under an organization
    nsg_params = {"name": organization['nsg_name'],
                  "templateID": nsg_temp.id,
                  "ZFBMatchAttribute": organization['match_type'],
                  "ZFBMatchValue": organization['match_value']}
    nsg_dev = NUNSGateway(data=nsg_params)
    metro_org.create_child(nsg_dev)
    return metro_org


def create_iso_file(metro_org, nsg_temp, nsgv_path):
    zfb_constants = module.params['zfb_constants']

    # Create an ISO file that's attached to nsgv vm
    job = NUJob()
    job.command = "GET_ZFB_INFO"
    zfb_constants['iso_params']['associatedEntityID'] = nsg_temp.id
    job.parameters = zfb_constants['iso_params']
    metro_org.create_child(job)
    subprocess.call("echo %s | base64 -d > %s/user_image.iso.gz"
                    % (job.result, nsgv_path), shell=True)
    sleep(1)
    # Copy ISO file to nsg-deploy files folder
    subprocess.call("gzip -f -d %s/user_image.iso.gz" % nsgv_path, shell=True)


def main():
    # Nsgv_path

    nsgv_path = module.params['nsgv_path']
    fact_name = module.params['fact_name']
    zfb_params = module.params['zfb_params']
    vsd_auth = module.params['vsd_auth']

    # Get VSD license
    vsd_license = ""
    try:
        with open(zfb_params['vsd_license_file'], 'r') as lf:
            vsd_license = lf.read()
    except Exception as e:
        module.fail_json(msg="ERROR: Failure reading file: %s" % e)
        sys.exit(1)

    # Create a session as csp user
    try:
        session = NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
    except Exception as e:
        module.fail_json(
            msg="ERROR: Could not establish connection to VSD API "
                "using %s: %s" % (vsd_auth, str(e)))
        sys.exit(1)

    nsg_already_configured = False

    # Create nsg templates and iso file
    if (not is_license_already_installed(csproot, vsd_license)):
        install_license(csproot, vsd_license)
    create_proxy_user(session)
    nsg_temp = get_nsg_gateway_template(csproot)
    if (nsg_temp is None):
        nsg_temp = create_nsg_gateway_template(csproot)
        vsc_temp = create_vsc_template(csproot)
        create_nsgv_ports(nsg_temp, vsc_temp)
        metro_org = create_nsg_device(csproot, nsg_temp)
    else:
        nsg_already_configured = True
        metro_org = csproot

    create_iso_file(metro_org, nsg_temp, nsgv_path)

    module.exit_json(changed=True,
                     ansible_facts={fact_name: nsg_already_configured})


arg_spec = dict(
    nsgv_path=dict(
        required=True,
        type='str'),
    fact_name=dict(
        required=True,
        type='str'),
    vsd_auth=dict(
        required=True,
        type='dict'),
    zfb_constants=dict(
        required=True,
        type='dict'),
    zfb_params=dict(
        required=True,
        type='dict'))

module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

if __name__ == '__main__':
    main()
