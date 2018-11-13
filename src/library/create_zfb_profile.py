#!/usr/bin/python

from vspk.v5_0 import NULicense, NUEnterprise, NUUser, NUNSPortTemplate
from vspk.v5_0 import NUInfrastructureGatewayProfile, NUNSGatewayTemplate
from vspk.v5_0 import NUInfrastructureVscProfile, NUVLANTemplate, NUJob
from vspk.v5_0 import NUNSGateway, NUVSDSession, NUUplinkConnection
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
      - Name of fact variable to state if NSGv is already configured.
    required:True
  vsd_license_file:
    description:
      - Set path to VSD license file.
    required:True
  vsd_auth:
    description:
      - Credentials for accessing VSD.  Attributes:
      - username
      - password
      - enterprise
      - api_url
    required:True
  zfb_constants:
    description:
      - Constant values for ZFB.  Attributes:
      - proxy_user
      - useTwoFactor
      - upgradeAction
      - network_port_type
      - access_port_type
      - iso_params
    required:True
  zfb_proxy_user:
    description:
      - Parameters for proxy user to be configured.  Attributes:
      - firstName
      - lastName
      - email
      - password
    required:True
  zfb_nsg:
    description:
      - Parameters required for an NSG profile for ZFB.  Attributes:
      - nsg_organization
      - nsg_name
      - nsg_template_name
      - match_type
      - match_value
      - ssh_service
    required:True
  zfb_ports:
    description:
      - Parameters required for an NSG ports for ZFB.  Attributes:
      - network_port.name
      - network_port.physicalName
      - access_port.name
      - access_port.physicalName
      - access_port.VLANRange
      - access_port.vlan_value
    required:True
  zfb_nsg_infra:
    description:
      - Parameters required for an NSG Infrastructure profile.  Attributes:
      - name
      - proxyDNSName
      - instanceSSHOverride
    required:True
  zfb_vsc_infra:
    description:
      - Parameters required for an VSC Infrastructure profile.  Attributes:
      - name
      - firstController
      - secondController
    required:True

'''

EXAMPLES = '''
- create_zfb_profile:
    nsgv_path: /tmp/ansible.1234
    fact_name: nsgv_already_configured,
    vsd_license_file: /data/vsd_license.txt
    vsd_auth:
        username: csproot
        password: csproot
        enterprise: csp
        api_url: https://localhost:8443
    zfb_constants:
        proxy_user: proxy
        useTwoFactor: False
        upgradeAction: NONE
        network_port_type: NETWORK
        access_port_type: ACCESS
        iso_params:
            mediaType: ISO
            associatedEntityType: nsgatewaytemplate
            NSGType: ANY
            associatedEntityID: update
    zfb_proxy_user:
        firstName: John
        lastName: Doe
        email: user@email.com
        password: pass
    zfb_nsg:
        nsg_organization: enterprise
        nsg_name: NSG1
        nsg_template_name: nsg_template
        match_type: ip_address
        match_value: 192.168.1.1
        ssh_service: false
    zfb_ports:
        network_port:
            name: port1_network
            physicalName: port1
        access_port:
            name: port2_access
            physicalName: port2
            VLANRange: "0-100"
            vlan_value: 20
    zfb_nsg_infra:
        name: nsg_infra
        proxyDNSName: vnsutil1.example.com
        instanceSSHOverride: true
    zfb_vsc_infra:
        name: vsc_infra
        firstController: 192.168.1.100
        secondController: 192.168.1.101
'''


def install_license(csproot, vsd_license):
    # Push the license
    test_license = NULicense(license=vsd_license)
    csproot.create_child(test_license)


def is_license_already_installed(csproot, vsd_license):
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
    zfb_proxy_user = module.params['zfb_proxy_user']
    zfb_constants = module.params['zfb_constants']

    # Create proxy user if not present
    cspenterprise = NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if zfb_constants['proxy_user'] not in lst_users:
        proxy_user = NUUser(first_name=zfb_proxy_user['firstName'],
                            last_name=zfb_proxy_user['lastName'],
                            user_name=zfb_constants['proxy_user'],
                            email=zfb_proxy_user['email'],
                            password=zfb_proxy_user['password'])
        cspenterprise.create_child(proxy_user)
        csprootuser = NUUser(id=session.me.id)
        csprootuser.fetch()
        # Add proxy user to root group
        csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                      'Root Group'")
        csprootgroup.assign([proxy_user, csprootuser], NUUser)


def create_nsg_infra_profile(csproot):
    infra_params = module.params['zfb_nsg_infra']
    zfb_constants = module.params['zfb_constants']

    nsg_infra = csproot.infrastructure_gateway_profiles.get_first(
        "name is '%s'" % infra_params['name'])

    if nsg_infra is None:
        infra_params['useTwoFactor'] = zfb_constants['useTwoFactor']
        infra_params['upgradeAction'] = zfb_constants['upgradeAction']
        nsg_infra = NUInfrastructureGatewayProfile(data=infra_params)
        csproot.create_child(nsg_infra)

    return nsg_infra


def create_nsg_gateway_template(csproot, nsg_infra):
    nsg_params = module.params['zfb_nsg']

    nsg_temp = csproot.ns_gateway_templates.get_first(
        "name is '%s'" % nsg_params['nsg_template_name'])

    if nsg_temp is None:
        nsg_temp = NUNSGatewayTemplate(name=nsg_params['nsg_template_name'])
        nsg_temp.infrastructure_profile_id = nsg_infra.id
        csproot.create_child(nsg_temp)

    return nsg_temp


def create_vsc_infra_profile(csproot):
    vsc_params = module.params['zfb_vsc_infra']

    vsc_infra = csproot.infrastructure_vsc_profiles.get_first(
        "name is '%s'" % vsc_params['name'])

    if vsc_infra is None:
        vsc_infra = NUInfrastructureVscProfile(data=vsc_params)
        csproot.create_child(vsc_infra)

    return vsc_infra


def create_nsgv_ports(nsg_temp, vsc_infra):
    port_params = module.params['zfb_ports']
    zfb_constants = module.params['zfb_constants']

    network_port = port_params['network_port']
    access_port = port_params['access_port']

    # Create network port
    port_temp = nsg_temp.ns_port_templates.get_first(
        "name is '%s'" % network_port['name'])

    if port_temp is None:
        network_port['portType'] = zfb_constants['network_port_type']
        port_temp = NUNSPortTemplate(data=network_port)
        nsg_temp.create_child(port_temp)
        # Attach vlan0 and vsc profile
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = '0'
        vlan_temp.associated_vsc_profile_id = vsc_infra.id
        port_temp.create_child(vlan_temp)

        uplink = NUUplinkConnection()
        uplink.mode = "Dynamic"
        uplink.role = "PRIMARY"
        vlan_temp.create_child(uplink)

    port_temp = nsg_temp.ns_port_templates.get_first(
        "name is '%s'" % access_port['name'])

    # Create access port
    if port_temp is None:
        vlan_id = access_port.pop('vlan_value')
        access_port['portType'] = zfb_constants['access_port_type']
        port_temp = NUNSPortTemplate(data=access_port)
        nsg_temp.create_child(port_temp)
        # Attach vlan
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = vlan_id
        port_temp.create_child(vlan_temp)


def create_enterprise(csproot, name):
    enterprise = csproot.enterprises.get_first(
        "name is '%s'" % name)

    if enterprise is None:
        enterprise = NUEnterprise(name=name)
        csproot.create_child(enterprise)

    return enterprise


def create_nsg_device(csproot, nsg_temp):
    nsg_params = module.params['zfb_nsg']
    nsg_infra = module.params['zfb_nsg_infra']

    # Create an ORG/Enterprise
    metro_org = create_enterprise(csproot, nsg_params['nsg_organization'])

    nsg_dev = metro_org.ns_gateways.get_first(
        "name is '%s'" % nsg_params['nsg_name'])

    if nsg_dev is None:
        # Create NSG device under an nsg
        nsg_data = {"name": nsg_params['nsg_name'],
                    "templateID": nsg_temp.id,
                    "ZFBMatchAttribute": nsg_params['match_type'],
                    "ZFBMatchValue": nsg_params['match_value'],
                    "personality": "NSG"}
        if nsg_infra["instanceSSHOverride"] == "ALLOWED":
            nsg_data["SSHService"] = nsg_params['ssh_service']

        nsg_dev = NUNSGateway(data=nsg_data)
        metro_org.create_child(nsg_dev)

    return metro_org


def has_nsg_configuration(csproot):
    nsg_params = module.params['zfb_nsg']

    enterprise = csproot.enterprises.get_first(
        "name is '%s'" % nsg_params['nsg_organization'])

    if enterprise is not None:
        nsg_dev = enterprise.ns_gateways.get_first(
            "name is '%s'" % nsg_params['nsg_name'])

        return nsg_dev is not None

    return False


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

    vsd_license_file = module.params['vsd_license_file']
    vsd_auth = module.params['vsd_auth']
    nsgv_path = module.params['nsgv_path']
    fact_name = module.params['fact_name']

    # Get VSD license
    vsd_license = ""
    try:
        with open(vsd_license_file, 'r') as lf:
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

    if has_nsg_configuration(csproot):
        nsg_already_configured = True

    create_proxy_user(session)

    nsg_infra = create_nsg_infra_profile(csproot)
    nsg_temp = create_nsg_gateway_template(csproot, nsg_infra)
    vsc_infra = create_vsc_infra_profile(csproot)
    create_nsgv_ports(nsg_temp, vsc_infra)
    metro_org = create_nsg_device(csproot, nsg_temp)

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
    vsd_license_file=dict(
        required=True,
        type='str'),
    vsd_auth=dict(
        required=True,
        type='dict'),
    zfb_constants=dict(
        required=True,
        type='dict'),
    zfb_proxy_user=dict(
        required=True,
        type='dict'),
    zfb_nsg=dict(
        required=True,
        type='dict'),
    zfb_ports=dict(
        required=True,
        type='dict'),
    zfb_nsg_infra=dict(
        required=True,
        type='dict'),
    zfb_vsc_infra=dict(
        required=True,
        type='dict'))

module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

if __name__ == '__main__':
    main()
