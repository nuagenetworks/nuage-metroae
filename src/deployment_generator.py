#!/usr/bin/env python

import jinja2
import os
import sys
import yaml

TEMPLATES_DIRECTORY = "src/deployment_templates"
DEPLOYMENTS_DIRECTORY = "deployments"


def usage():
    print "Converts single user data file into a current"
    print "deployment configuration under the %s/ directory." % (
        DEPLOYMENTS_DIRECTORY)
    print ""
    print "Usage:"
    print "    " + " ".join([sys.argv[0],
                             "<user_input_file>",
                             "<deployment_name>"])
    print ""


def read_user_input(user_input_file):
    with open(user_input_file, "r") as file:
        user_input_contents = file.read().decode("utf-8")

    var_dict = yaml.safe_load(user_input_contents)

    return var_dict


def write_deployments(var_dict, deployment_name):

    deployment_dir = os.path.join(DEPLOYMENTS_DIRECTORY, deployment_name)
    if not os.path.exists(deployment_dir):
        os.makedirs(deployment_dir)

    deployment_template_files = os.listdir(TEMPLATES_DIRECTORY)

    for deployment_template_file in deployment_template_files:
        deployment_filename = deployment_template_file.split(".")[0]
        deployment_file = deployment_filename + ".yml"
        write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, deployment_template_file),
                              os.path.join(deployment_dir, deployment_file), var_dict)
        # To write a single deployment file, use this syntax:
        # write_deployment_file(os.path.join(TEMPLATES_DIRECTORY, "stcvs.j2"),
        #                       os.path.join(deployment_dir, "stcvs.yml"),
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

    if len(sys.argv) != 3:
        usage()
        exit(1)

    user_input_file = sys.argv[1]
    deployment_name = sys.argv[2]

    var_dict = read_user_input(user_input_file)
    write_deployments(var_dict, deployment_name)


if __name__ == '__main__':
    main()
