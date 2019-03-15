#!/usr/bin/env python

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


def read_user_input(user_input_file):
    with open(user_input_file, "r") as file:
        user_input_contents = file.read().decode("utf-8")

    var_dict = yaml.safe_load(user_input_contents)

    return var_dict


def write_deployment(var_dict, deployment_name):

    deployment_dir = os.path.join(DEPLOYMENTS_DIRECTORY, deployment_name)
    if not os.path.exists(deployment_dir):
        os.makedirs(deployment_dir)

    deployment_temps = os.listdir(TEMPLATES_DIRECTORY)

    for deployment_temp in deployment_temps:
        tmp = deployment_temp.split(".", 1)[0]
        deployment_file = tmp + ".yml"
        write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, deployment_temp),
                              os.path.join(deployment_dir, deployment_file), var_dict)

    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "common.j2"),
    #                       os.path.join(deployment_dir, "common.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vsds.j2"),
    #                       os.path.join(deployment_dir, "vsds.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vscs.j2"),
    #                       os.path.join(deployment_dir, "vscs.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vstats.j2"),
    #                       os.path.join(deployment_dir, "vstats.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "nsgvs.j2"),
    #                       os.path.join(deployment_dir, "nsgvs.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vcins.j2"),
    #                       os.path.join(deployment_dir, "vcins.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vnsutils.j2"),
    #                       os.path.join(deployment_dir, "vnsutils.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "vrss.j2"),
    #                       os.path.join(deployment_dir, "vrss.yml"),
    #                       var_dict)
    # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "credentials.j2"),
    #                       os.path.join(deployment_dir, "credentials.yml"),
    #                       var_dict)


def write_deployment_file(template_file, to_file, var_dict):
    print "Writing " + to_file

    with open(template_file, "r") as file:
        template_string = file.read().decode("utf-8")

    template = jinja2.Template(template_string,
                               autoescape=False,
                               undefined=jinja2.StrictUndefined)

    var_file_contents = template.render(var_dict)

    with open(to_file, "w") as file:
        file.write(var_file_contents.encode("utf-8"))


def main():

    print """
Deprecation Notice: The convert_build_vars_to_deployment tool is
not actively updated for new features and will be removed in MetroAE
v3.4.0. Users of this tool should either edit deployment files directly or
modify their process to take advantage of the jinja2 templates available in
src/deployment_templates to auto-generate deployment files.

"""

    if len(sys.argv) != 3:
        usage()
        exit(1)

    user_input_file = sys.argv[1]
    deployment_name = sys.argv[2]

    var_dict = read_user_input(user_input_file)
    write_deployment(var_dict, deployment_name)


if __name__ == '__main__':
    main()
