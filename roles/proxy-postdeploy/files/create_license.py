from vspk.v4_0 import *
from config import *
import sys
import subprocess
from time import sleep
import argparse

def install_license(csp_user, vsd_license):
    csproot = csp_user
    #Clear any existing license
    installed_licenses = csproot.licenses.get()
    for lic in installed_licenses:
        lic.delete()

    #Push the license
    test_license = NULicense(license=vsd_license)
    csproot.create_child(test_license)

def create_proxy_user(session):
    #create proxy user if not present
    cspenterprise = NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if 'proxy' not in lst_users:
        proxy_user = NUUser(first_name=user_params['firstName'], 
                            last_name=user_params['lastName'], 
                            user_name=user_params['userName'],
		            email=user_params['email'], 
                            password=user_params['password']
                           )
        cspenterprise.create_child(proxy_user)
        csprootuser = NUUser(id=session.me.id)
        csprootuser.fetch()
        #Add proxy user to root group
        csprootgroup = cspenterprise.groups.get_first(filter="name =='Root Group'")
        csprootgroup.assign([proxy_user, csprootuser], NUUser)

def create_nsg_gateway_template(csp_user):
    csproot = csp_user
    #Fetch current infra profiles
    nsg_temp = NUNSGatewayTemplate()
    infra_profiles = csproot.infrastructure_gateway_profiles.get()
    lst_infra_names = [infra.name for infra in infra_profiles]
    if vns_nsg['name'] not in lst_infra_names:
        #Create infra profile
        nsg_infra = NUInfrastructureGatewayProfile(data = vns_nsg)
        csproot.create_child(nsg_infra)
        #Attach the infra profile to NSG template
        vns_infra_profile = csproot.infrastructure_gateway_profiles.get_first(filter="name == '%s'" %vns_nsg['name'])
        infra_id = vns_infra_profile.id
        nsg_temp.name = 'metro_test'
        nsg_temp.infrastructure_profile_id=infra_id
        csproot.create_child(nsg_temp)
    return nsg_temp

def create_vsc_template(csp_user,active_ip,standby_ip):
    csproot = csp_user
    #Fetch current infra vsc profile
    vns_vsc['firstController'] = active_ip
    vns_vsc['secondController'] = standby_ip
    vsc_temp = NUInfrastructureVscProfile(data = vns_vsc)
    infra_vsc_profiles = csproot.infrastructure_vsc_profiles.get()
    lst_infra_vsc = [infra.name for infra in infra_vsc_profiles]
    if vns_vsc['name'] not in lst_infra_vsc:
        #Create infra vsc profile
        csproot.create_child(vsc_temp)
    return vsc_temp

def create_nsgv_ports(nsg_temp,vsc_temp):
    #Create network port
    port_info = nsg_temp.ns_port_templates.get()
    lst_port_name = [port.name for port in port_info]
    if nsg_port['ntwrk_port']['name'] not in lst_port_name:
        port_temp = NUNSPortTemplate(data = nsg_port['ntwrk_port']) 
        nsg_temp.create_child(port_temp)
        #Attach vlan0 and vsc profile
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = '0'
        vlan_temp.associated_vsc_profile_id = vsc_temp.id
        port_temp.create_child(vlan_temp)

    #Create access port
    if nsg_port['access_port']['name'] not in lst_port_name:
        port_temp= NUNSPortTemplate(data = nsg_port['access_port'])
        nsg_temp.create_child(port_temp)
        #Attach vlan
        vlan_temp = NUVLANTemplate()
        vlan_temp.value = '20'
        port_temp.create_child(vlan_temp)

def create_nsg_device(csp_user,nsg_temp):
    csproot = csp_user
    #Create an ORG/Enterprise
    metro_org = NUEnterprise(name='metro-vns')
    csproot.create_child(metro_org)

    #Create NSG device under metro org
    nsg_dev = NUNSGateway(name='nsgv_test')
    nsg_dev.template_id = nsg_temp.id
    metro_org.create_child(nsg_dev)

def create_iso_file(csp_user,nsg_temp,nsgv_path):
    csproot = csp_user
    #Create an ISO file that's attached to nsgv vm
    job = NUJob()
    job.command = "GET_ZFB_INFO"
    iso_params["associatedEntityID"] = nsg_temp.id
    job.parameters = iso_params
    csproot.create_child(job)
    subprocess.call("echo %s | base64 -d > test.iso.gz" %job.result, shell=True)
    sleep(1)

    #Extract ISO file and copy to nsg-deploy templates
    subprocess.call("gzip -f -d test.iso.gz", shell=True)
    sleep(1)
    subprocess.call("cp test.iso %s" %nsgv_path, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("vsd_ip_fqdn", type=str,
                        help="Set VSD IP address or VSD FQDN.")
    parser.add_argument("active_controller", type=str,
                        help="Set active controller IP.")
    parser.add_argument("standby_controller", type=str,
                        help="Set standby controller IP.")
    parser.add_argument("vsd_license", type=str,
                        help="License to operate VSD architect.")
    parser.add_argument("playbook_dir", type=str,
                        help="Set path to playbook directory.")
    args = parser.parse_args()

    #set vsd url
    vsd_url = "https://%s:8443" %args.vsd_ip_fqdn
    csp['api_url'] = vsd_url
    print csp
  
    #set active/standby controller ip's
    active_ip = args.active_controller
    standby_ip = args.standby_controller

    #License
    vsd_license = args.vsd_license
    
    #nsgv_path
    nsgv_path = args.playbook_dir+'/roles/nsgv-deploy/templates/user_image.iso'
    
    #Create a session as csp user
    session = NUVSDSession(**csp)
    session.start()
    csproot = session.user

    #Create nsg templates and iso file
    install_license(csproot,vsd_license)
    create_proxy_user(session)
    nsg_temp = create_nsg_gateway_template(csproot)
    vsc_temp = create_vsc_template(csproot,active_ip,standby_ip)
    create_nsgv_ports(nsg_temp,vsc_temp)
    create_nsg_device(csproot,nsg_temp)
    create_iso_file(csproot,nsg_temp,nsgv_path)

