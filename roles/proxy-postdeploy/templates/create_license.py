from vspk.v4_0 import *
from config import *
import sys
import subprocess
from time import sleep


#vsd url
vsd_url = sys.argv[1]
#csp creds
csp = {'username':  'csproot',
       'password':  'csproot',
       'enterprise': 'csp',
       'api_url':   'https://%s:8443' %vsd_url
      }

#Create a session as csp user
session = NUVSDSession(**csp)
session.start()
csproot = session.user

#Clear any existing license
installed_licenses = csproot.licenses.get()
for lic in installed_licenses:
    lic.delete()

#Push the license
test_license = NULicense(license=vsd_license)
csproot.create_child(test_license)

#Fetch current users and create proxy user if not present
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
    csprootgroup = cspenterprise.groups.get_first(filter="name =='Root Group'")
    csprootgroup.assign([proxy_user, csprootuser], NUUser)

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

#Fetch current infra vsc profile
vsc_infra = NUInfrastructureVscProfile(data = vns_vsc)
infra_vsc_profiles = csproot.infrastructure_vsc_profiles.get()
lst_infra_vsc = [infra.name for infra in infra_vsc_profiles]
if vns_vsc['name'] not in lst_infra_vsc:
    #Create infra vsc profile
    csproot.create_child(vsc_infra)

#Create network port
port_info = nsg_temp.ns_port_templates.get()
lst_port_name = [port.name for port in port_info]
if nsg_port['ntwrk_port']['name'] not in lst_port_name:
    port_temp = NUNSPortTemplate(data = nsg_port['ntwrk_port']) 
    nsg_temp.create_child(port_temp)
    #Attach vlan0 and vsc profile
    vlan_temp = NUVLANTemplate()
    vlan_temp.value = '0'
    vlan_temp.associated_vsc_profile_id = vsc_infra.id
    port_temp.create_child(vlan_temp)

#Create access port
if nsg_port['access_port']['name'] not in lst_port_name:
   port_temp= NUNSPortTemplate(data = nsg_port['access_port'])
   nsg_temp.create_child(port_temp)
   #Attach vlan
   vlan_temp = NUVLANTemplate()
   vlan_temp.value = '20'
   port_temp.create_child(vlan_temp)

#Create an ORG/Enterprise
metro_org = NUEnterprise(name='metro-vns')
csproot.create_child(metro_org)

#Create NSG device under metro org
nsg_dev = NUNSGateway(name='nsgv_test')
nsg_dev.template_id = nsg_temp.id
metro_org.create_child(nsg_dev)

#Create an ISO file that's attached to nsgv vm
job = NUJob()
job.command = "GET_ZFB_INFO"
params["associatedEntityID"] = nsg_temp.id
job.parameters = iso_params
csproot.create_child(job)
subprocess.call("echo %s | base64 -d > test.iso.gz" %job.result, shell=True)
sleep(1)

#Extract ISO file and copy to nsg-deploy templates
subprocess.call("gzip -f -d test.iso.gz", shell=True)
sleep(1)
subprocess.call("cp test.iso /root/test.iso", shell=True)
