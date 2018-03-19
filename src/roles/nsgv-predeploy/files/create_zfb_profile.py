from vspk.v4_0 import NULicense, NUEnterprise, NUUser, NUNSPortTemplate
from vspk.v4_0 import NUInfrastructureGatewayProfile, NUNSGatewayTemplate
from vspk.v4_0 import NUInfrastructureVscProfile, NUVLANTemplate, NUJob
from vspk.v4_0 import NUNSGateway, NUVSDSession
import subprocess
import yaml
import sys
from time import sleep
import argparse


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
    csproot = csp_user
    organization = zfb_params['organization']
    # Create an ORG/Enterprise
    metro_org = NUEnterprise(name=organization['name'])
    csproot.create_child(metro_org)

    # Create NSG device under an organization
    nsg_dev = NUNSGateway(name=organization['nsg_name'])
    nsg_dev.template_id = nsg_temp.id
    metro_org.create_child(nsg_dev)


def create_iso_file(csp_user, nsg_temp, nsgv_path):
    csproot = csp_user
    # Create an ISO file that's attached to nsgv vm
    job = NUJob()
    job.command = "GET_ZFB_INFO"
    zfb_constants['iso_params']['associatedEntityID'] = nsg_temp.id
    job.parameters = zfb_constants['iso_params']
    csproot.create_child(job)
    subprocess.call("echo %s | base64 -d > %s/user_image.iso.gz"
                    % (job.result, nsgv_path), shell=True)
    sleep(1)
    # Copy ISO file to nsg-deploy files folder
    subprocess.call("gzip -f -d %s/user_image.iso.gz" % nsgv_path, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("working_dir", type=str,
                        help="Set path to working directory.")
    parser.add_argument("nsgv_path", type=str, help="Set path to NSGV ISO\
                        output directory")
    args = parser.parse_args()

    # Nsgv_path
    nsgv_path = args.nsgv_path

    # Get ZFB related parameters
    try:
        with open(args.working_dir + '/zfb_vars.yml', 'r') as fh:
            zfb_params = yaml.load(fh)
        vars_file = '/roles/nsgv-predeploy/vars/main.yml'
        with open(args.working_dir + vars_file, 'r') as fo:
            zfb_constants = yaml.load(fo)
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
    except Exception as e:
        print("ERROR: Could not establish connection to VSD API using %s" %
              zfb_params['csp'])
        print("ERROR: Exception: %s" % e)
        sys.exit(1)

    # Create nsg templates and iso file
    if (not is_license_already_installed(csproot, vsd_license)):
        install_license(csproot, vsd_license)
    create_proxy_user(session)
    nsg_temp = get_nsg_gateway_template(csproot)
    if (nsg_temp is None):
        nsg_temp = create_nsg_gateway_template(csproot)
        vsc_temp = create_vsc_template(csproot)
        create_nsgv_ports(nsg_temp, vsc_temp)
        create_nsg_device(csproot, nsg_temp)
    else:
        print("NSG ALREADY CONFIGURED")

    create_iso_file(csproot, nsg_temp, nsgv_path)
