#!/usr/bin/env python
from client import (
    VsdClient
)
import os
import sys

vsd_service_ip = sys.argv[1]
vsd_demo = VsdClient(vsd_service_ip)

temp_dir = '/tmp/vsd_license'
license_file = os.path.join(temp_dir, 'vsp_base_license.txt')
with open(license_file, "r") as lic_file:
    vsd_licenses = lic_file.readlines()
    for vsd_license in vsd_licenses:
        vsd_demo.install_license(vsd_license.strip())

vsd_demo.add_csproot_to_cms_group()
domains = vsd_demo.get_domains()
if domains:
    print domains
subnets = vsd_demo.get_subnets()
if subnets:
    print subnets
vms = vsd_demo.get_vms()
if vms:
    print vms
