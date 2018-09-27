#!/usr/bin/python

import jinja2
from netaddr import IPAddress
import os
import sys
import yaml

TEMPLATES_DIRECTORY = "src/deployment_templates"
DEPLOYMENTS_DIRECTORY = "deployments"


def usage():
    print "Converts the deprecated build_vars.yml format file into a current"
    print "deployment configuration under the %s/ directory." % (
        DEPLOYMENTS_DIRECTORY)
    print ""
    print "Usage:"
    print "    " + " ".join([sys.argv[0],
                             "<build_vars_file>",
                             "<deployment_name>"])
    print ""


def read_build_vars(build_vars_file):
    with open(build_vars_file, "r") as file:
        var_dict = yaml.safe_load(file.read())

    var_dict["generator_script"] = "conversion from " + build_vars_file

    if "dns_domain" not in var_dict:
        dns_domain = var_dict["vsd_fqdn_global"].split(".")
        dns_domain = ".".join(dns_domain[1:])
        var_dict["dns_domain"] = dns_domain

    return var_dict


def resolve_missing_variables(var_dict):
    var_dict["libnetwork_cluster_store_host"] = "localhost"

    if "myvsds" in var_dict:
        var_dict["vsds"] = var_dict["myvsds"]
        flatten_vcenter(var_dict["vsds"])
        convert_mask_to_length(var_dict["vsds"])
        add_upgrade_vm_name(var_dict["vsds"])
    else:
        var_dict["vsds"] = list()

    if "myvscs" in var_dict:
        var_dict["vscs"] = var_dict["myvscs"]
        flatten_vcenter(var_dict["vscs"])
        convert_mask_to_length(var_dict["vscs"])
        add_upgrade_vm_name(var_dict["vscs"])
    else:
        var_dict["vscs"] = list()

    if "myvstats" in var_dict:
        var_dict["vstats"] = var_dict["myvstats"]
        flatten_vcenter(var_dict["vstats"])
        convert_mask_to_length(var_dict["vstats"])
        add_upgrade_vm_name(var_dict["vstats"])
    else:
        var_dict["vstats"] = list()

    if "mynsgvs" in var_dict:
        var_dict["nsgvs"] = var_dict["mynsgvs"]
        flatten_vcenter(var_dict["nsgvs"])
        convert_mask_to_length(var_dict["nsgvs"])
        add_upgrade_vm_name(var_dict["nsgvs"])
    else:
        var_dict["nsgvs"] = list()

    if "myvcins" in var_dict:
        var_dict["vcins"] = var_dict["myvcins"]
        flatten_vcenter(var_dict["vcins"])
        convert_mask_to_length(var_dict["vcins"])
        add_upgrade_vm_name(var_dict["vcins"])
    else:
        var_dict["vcins"] = list()

    if "myvnsutils" in var_dict:
        var_dict["vnsutils"] = var_dict["myvnsutils"]
        flatten_vcenter(var_dict["vnsutils"])
        convert_mask_to_length(var_dict["vnsutils"])
        add_upgrade_vm_name(var_dict["vnsutils"])
    else:
        var_dict["vnsutils"] = list()

    if "myvrss" in var_dict:
        var_dict["vrss"] = var_dict["myvrss"]
        flatten_vcenter(var_dict["vrss"])
        convert_mask_to_length(var_dict["vrss"])
        add_upgrade_vm_name(var_dict["vrss"])
    else:
        var_dict["vrss"] = list()

    if "vcenter" in var_dict:
        flatten_vcenter([var_dict])
        if "ovftool" in var_dict["vcenter"]:
            var_dict["vcenter_ovftool"] = var_dict["vcenter"]["ovftool"]


def flatten_vcenter(component_list):
    for component in component_list:
        if "vcenter" in component:
            if "username" in component["vcenter"]:
                component["vcenter_username"] = \
                    component["vcenter"]["username"]
            if "password" in component["vcenter"]:
                component["vcenter_password"] = \
                    component["vcenter"]["password"]
            if "datacenter" in component["vcenter"]:
                component["vcenter_datacenter"] = \
                    component["vcenter"]["datacenter"]
            if "cluster" in component["vcenter"]:
                component["vcenter_cluster"] = \
                    component["vcenter"]["cluster"]
            if "datastore" in component["vcenter"]:
                component["vcenter_datastore"] = \
                    component["vcenter"]["datastore"]


def convert_mask_to_length(component_list):
    for component in component_list:
        if "mgmt_netmask" in component:
            mask = component["mgmt_netmask"]
            component["mgmt_ip_prefix"] = IPAddress(mask).netmask_bits()
        if "mgmt_netmask_prefix" in component:
            mask = component["mgmt_netmask_prefix"]
            component["mgmt_ip_prefix"] = mask
        if "ctrl_netmask_prefix" in component:
            mask = component["ctrl_netmask_prefix"]
            component["ctrl_ip_prefix"] = mask


def add_upgrade_vm_name(component_list):
    for component in component_list:
        if "upgrade_vmname" not in component and "vmname" in component:
            component["upgrade_vmname"] = "new-" + component["vmname"]


def write_deployment(var_dict, deployment_name):

    deployment_dir = os.path.join(DEPLOYMENTS_DIRECTORY, deployment_name)
    if not os.path.exists(deployment_dir):
        os.makedirs(deployment_dir)

    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "common.j2"),
                          os.path.join(deployment_dir, "common.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vsds.j2"),
                          os.path.join(deployment_dir, "vsds.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vscs.j2"),
                          os.path.join(deployment_dir, "vscs.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vstats.j2"),
                          os.path.join(deployment_dir, "vstats.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "nsgvs.j2"),
                          os.path.join(deployment_dir, "nsgvs.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vcins.j2"),
                          os.path.join(deployment_dir, "vcins.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vnsutils.j2"),
                          os.path.join(deployment_dir, "vnsutils.yml"),
                          var_dict)
    write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vrss.j2"),
                          os.path.join(deployment_dir, "vrss.yml"),
                          var_dict)

    if "vcenter" in var_dict:
        write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vcenter.j2"),
                              os.path.join(deployment_dir, "vcenter.yml"),
                              var_dict)


def write_deployment_file(template_file, to_file, var_dict):
    print "Writing " + to_file

    with open(template_file, "r") as file:
        template_string = file.read()

    template = jinja2.Template(template_string,
                               autoescape=False,
                               undefined=jinja2.StrictUndefined)

    var_file_contents = template.render(var_dict)

    with open(to_file, "w") as file:
        file.write(var_file_contents)


def main():
    if len(sys.argv) != 3:
        usage()
        exit(1)

    build_vars_file = sys.argv[1]
    deployment_name = sys.argv[2]

    var_dict = read_build_vars(build_vars_file)
    resolve_missing_variables(var_dict)
    write_deployment(var_dict, deployment_name)


if __name__ == '__main__':
    main()
