#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import traceback
import yaml

from generate_example_from_schema import ExampleFileGenerator

METROAE_CONTACT = "devops@nuagenetworks.net"

WIZARD_SCRIPT = """

- message:
    text: |

      Thank you for using MetroÆ!

      This wizard will walk you through the setup process of MetroÆ
      step-by-step and ensure that all prerequisites are satisfied.

      For assistance please contact: {contact}

- list_steps: {}
  description: |

      The following steps will be performed:

- step: Verify proper MetroÆ installation
  description: |
      This step will verify that the MetroÆ tool has been properly installed
      with all required libraries present and with proper versions.
  verify_install:
    missing_msg: |

      There are missing libraries that are required for MetroÆ to operate.
      We would like to run setup to install these.  The command is
      "sudo ./metro-setup.sh".  This requires sudo access and may ask for root
      password.

- step: Unzip image files
  description: |
      This step will unzip the image files needed for the VSP components.  The
      source zip files can be downloaded from Nokia OLCS:

      https://support.alcatel-lucent.com/portal/web/support

      For upgrade: Specify the image file versions you are upgrading to.
  unzip_images: {}

- step: Create/read deployment
  description: |
      This step will create a starter deployment or read an existing one and
      begin filling it out.  A deployment is a configuration set for MetroÆ and
      describes the properties of each component.  There is support for
      multiple deployments each in their own directory.
  create_deployment: {}

- step: Common deployment file, DNS and NTP
  description: |
      This step will create or read an existing common.yml deployment file and
      begin filling it out.  This file provides global parameters for the
      deployment common to all components.  We will also setup DNS and NTP
      during this step.
  create_common:
    dns_setup_msg: |

      We will begin setting up DNS.  MetroÆ requires that most components have
      hostname to ip address DNS mappings defined before running workflows.
      Having DNS setup before continuing will allow this wizard to
      auto-discover component IP addresses.
    ntp_setup_msg: |

      We will now setup NTP.  An NTP server is required for the VSP components
      being installed/upgraded to keep their times synchronized.
    vsd_fqdn_msg: |
      Please enter the Fully Qualified Domain Name (FQDN) for the VSD.  If
      clustered, use the XMPP FQDN, for standalone use the FQDN of the VSD.

- message:
    text: |

      The wizard is complete!

"""

STANDARD_FIELDS = ["step", "description"]


class Wizard(object):

    def __init__(self, script=WIZARD_SCRIPT):
        self.state = dict()
        self.progress_display_count = 0
        self.progress_display_rate = 1

        if "NON_INTERACTIVE" in os.environ:
            self.args = list(sys.argv)
            self.args.pop(0)
        else:
            self.args = list()

        self.script = yaml.safe_load(script)
        self._validate_actions()

    def __call__(self):
        self._run_script()

    #
    # Script Actions
    #

    def message(self, action, data):
        raw_msg = self._get_field(data, "text")
        format_msg = raw_msg.format(contact=METROAE_CONTACT)
        self._print(format_msg)

    def list_steps(self, action, data):
        for step in self.script:
            if "step" in step:
                self._print("  - " + step["step"])

    def verify_install(self, action, data):
        self._print("\nVerifying MetroÆ installation")

        missing = self._verify_pip()
        yum_missing = self._verify_yum()

        missing.extend(yum_missing)

        if len(missing) == 0:
            self._print("\nMetroÆ Installation OK!")
        else:
            self._print("\nYour MetroÆ installation is missing libraries:\n")
            self._print("\n".join(missing))
            self._print(self._get_field(data, "missing_msg"))
            choice = self._input("Do you want to run setup now?", 0,
                                 ["(Y)es", "(n)o"])

            if choice != 1:
                self._run_setup()

    def unzip_images(self, action, data):
        valid = False
        while not valid:
            zip_dir = self._input("Specify the directory containing the zip "
                                   "files from OLCS", "")

            if zip_dir == "" or not os.path.exists(zip_dir):
                choice = self._input(
                    "Directory not found, would you like to skip unzipping",
                    0, ["(Y)es", "(n)o"])
                if choice != 1:
                    self._print("Skipping unzip step...")
                    return
            elif not os.path.isdir(zip_dir):
                self._print("%s is not a directory, please enter the directory"
                            " containing the zipped files" % zip_dir)
            else:
                valid = True

        unzip_dir = self._input("Specify the directory to unzip to")

        self.state["nuage_unzipped_files_dir"] = unzip_dir

        choice = self._input(
            "Unzip %s to %s" % (zip_dir, unzip_dir),
            0, ["(Y)es", "(n)o"])
        if choice == 0:
            self._run_unzip(zip_dir, unzip_dir)
        else:
            self._print("Skipping unzip step...")

    def create_deployment(self, action, data):
        valid = False
        while not valid:
            deployment_name = self._input(
                "Deployment name (will be a directory)", "default")
            if "/" in deployment_name:
                self._print("\nA deployment name cannot contain a slash "
                            "as it will be a directory name")
            elif " " in deployment_name:
                self._print("\nA deployment name can contain a space, but it "
                            "will always have to be specified with quotes")
                choice = self._input("Do you want use it?", 0,
                                     ["(Y)es", "(n)o"])
                if choice != 1:
                    valid = True
            else:
                valid = True

        found = False
        deployment_dir = os.path.join("deployments", deployment_name)
        if os.path.isdir(deployment_dir):
            self._print("\nDeployment was found")
            found = True
        else:
            self._print("")
            choice = self._input('Create deployment: "%s"?' % deployment_name,
                                 0, ["(Y)es", "(n)o"])
            if choice == 1:
                self._print("Skipping deployment creation.")
                return

        self._print("Deployment directory: " + deployment_dir)
        self.state["deployment_name"] = deployment_name
        self.state["deployment_dir"] = deployment_dir

        if not found:
            os.mkdir(deployment_dir)

    def create_common(self, action, data):
        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        deployment_file = os.path.join(deployment_dir, "common.yml")
        if os.path.isfile(deployment_file):
            deployment = self._read_deployment_file(deployment_file)
        else:
            self._print(deployment_file + " not found. It will be created.")
            deployment = dict()

        self._setup_dns(deployment, data)

        self._setup_ntp(deployment, data)

        if "nuage_unzipped_files_dir" in self.state:
            if ("nuage_unzipped_files_dir" not in deployment or
                    deployment["nuage_unzipped_files_dir"] == ""):
                deployment["nuage_unzipped_files_dir"] = (
                    self.state["nuage_unzipped_files_dir"])

        self._generate_deployment_file("common", deployment_file, deployment)

    #
    # Private class internals
    #

    def _print(self, msg):
        print msg

    def _print_progress(self):
        if self.progress_display_count % self.progress_display_rate == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        self.progress_display_count += 1

    def _input(self, prompt=None, default=None, choices=None):
        input_prompt = self._get_input_prompt(prompt, default, choices)
        value = None

        if "NON_INTERACTIVE" in os.environ:
            if len(self.args) < 1:
                raise Exception(
                    "Out of args for non-interactive input for %s" %
                    input_prompt)
            user_value = self.args.pop(0)
            if prompt is not None:
                self._print(prompt)
            self._print("From args: " + user_value)
            value = self._validate_input(user_value, default,
                                         choices)
            if value is None:
                raise Exception("Invalid non-interactive input for %s%s" %
                                (input_prompt, user_value))

        else:
            while value is None:
                user_value = raw_input(input_prompt)
                value = self._validate_input(user_value, default, choices)

        return value

    def _get_input_prompt(self, prompt=None, default=None, choices=None):

        input_prompt = ""

        if choices is not None:
            input_prompt += "\n".join(choices)
            input_prompt += "\n\n"

            short_choices = self._get_short_choices(choices, default)

            if prompt is not None:
                input_prompt += prompt
                input_prompt += " "

            input_prompt += "[%s]" % ("/".join(short_choices))
        else:
            default_sep = ""
            if prompt is not None:
                input_prompt += prompt
                default_sep = " "

            if default is not None:
                input_prompt += "%s[%s]" % (default_sep, default)

        input_prompt += ": "

        return input_prompt

    def _validate_input(self, user_value, default=None, choices=None):
        value = None
        if user_value == "":
            if default is not None:
                return default
            else:
                self._print("\nRequired field, please enter a value\n")
                return None

        if choices is not None:
            value = self._match_choice(user_value, choices)
            if value is None:
                self._print(
                    "\nValue is not a valid choice, please reenter\n")
        else:
            value = user_value

        return value

    def _get_short_choices(self, choices, default=None):
        short_choices = list()
        for i, choice in enumerate(choices):

            start_paren_idx = choice.find("(")
            if start_paren_idx >= 0:
                short_value = choice[start_paren_idx + 1]
            else:
                short_value = choice[0]

            if default == i:
                short_value = short_value.upper()
            else:
                short_value = short_value.lower()

            short_choices.append(short_value)

        return short_choices

    def _match_choice(self, user_value, choices):
        short_choices = self._get_short_choices(choices)
        for i, short_choice in enumerate(short_choices):
            if user_value.lower() == short_choice:
                return i

        return None

    def _validate_actions(self):
        for action in self.script:
            self._validate_action(action)

    def _validate_action(self, action):
        if type(action) == dict:
            action_name = self._get_action_name(action)
            if action_name.startswith("_") or not hasattr(self, action_name):
                raise Exception(
                    "Invalid wizard script format - %s not a valid action" %
                    action_name)
        else:
            raise Exception("Invalid wizard script format - action not a dict")

    def _run_script(self):
        current_action_idx = 0

        while current_action_idx < len(self.script):
            current_action = self.script[current_action_idx]
            if "step" in current_action:
                self._display_step(current_action)
                choice = self._input(None, 0, ["(C)ontinue",
                                               "(b)ack",
                                               "(s)kip",
                                               "(q)uit"])
                if choice == 1:
                    current_action_idx -= 1
                    continue
                if choice == 2:
                    current_action_idx += 1
                    continue
                if choice == 3:
                    self._print("Exiting MetroÆ wizard. All progress made has"
                                " been saved.")
                    exit(0)

            self._run_action(current_action)
            current_action_idx += 1

    def _display_step(self, action):
        self._print("")

        if "step" in action:
            self._print("**** " + action["step"] + " ****\n")

        if "description" in action:
            self._print(action["description"])

    def _run_action(self, action):
        action_name = self._get_action_name(action)
        action_func = getattr(self, action_name)
        data = action[action_name]
        action_func(action, data)

    def _get_action_name(self, action):
        keys = action.keys()
        for standard_field in STANDARD_FIELDS:
            if standard_field in keys:
                keys.remove(standard_field)
        if len(keys) != 1:
            raise Exception(
                "Invalid wizard script format - could not deterimine action")
        return keys[0]

    def _get_field(self, data, field_name):
        if type(data) == dict:
            if field_name in data:
                return data[field_name]
            else:
                raise Exception(
                    "Invalid wizard script format - data has no %s field" %
                    field_name)
        else:
            raise Exception("Invalid wizard script format - data not a dict")

    def _run_shell(self, cmd_str):
        process = subprocess.Popen(cmd_str,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        output_lines = list()
        rc = self._capture_output(process, output_lines)
        self.progress_display_rate = 1
        return rc, output_lines

    def _capture_output(self, process, output_lines):
        while True:
            retcode = process.poll()
            if retcode is None:
                line = process.stdout.readline().rstrip("\n")
                output_lines.append(line)
                self._print_progress()
            else:
                # Flush stdout buffer
                lines = process.stdout.read()
                for line in lines.split("\n"):
                    output_lines.append(line)
                    self._print_progress()

                return retcode

    def _verify_pip(self):
        try:
            rc, output_lines = self._run_shell("pip freeze")
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("pip freeze exit-code: %d" % rc)

            with open("pip_requirements.txt", "r") as f:
                required_libraries = f.read().split("\n")

        except Exception as e:
            self._print("\nAn error occurred while reading pip libraries: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)
            return ["Could not deterimine pip libraries"]

        return self._compare_libraries(required_libraries, output_lines)

    def _verify_yum(self):
        try:
            self.progress_display_rate = 30
            rc, output_lines = self._run_shell("yum list")
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("yum list exit-code: %d" % rc)

            with open("yum_requirements.txt", "r") as f:
                required_libraries = f.read().split("\n")

        except Exception as e:
            self._print("\nAn error occurred while reading yum libraries: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)
            return ["Could not deterimine yum libraries"]

        return self._compare_libraries(required_libraries, output_lines)

    def _run_setup(self):
        cmd = "sudo ./metro-setup.sh"
        self._print("Command: " + cmd)
        self._print("Running setup (may ask for sudo password)")
        try:
            rc, output_lines = self._run_shell(cmd)
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("metro-setup.sh exit-code: %d" % rc)

            self._print("\nMetroÆ setup completed successfully!")
        except Exception as e:
            self._print("\nAn error occurred while running setup: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)

    def _compare_libraries(self, required_libraries, installed_libraries):
        missing = list()
        for req_lib in required_libraries:
            if req_lib.startswith("@"):
                continue

            req_lib_name = req_lib.split("=")[0]

            found = False
            for inst_lib in installed_libraries:
                if inst_lib.lower().startswith(req_lib_name.lower()):
                    found = True
                    if not inst_lib.lower().startswith(req_lib.lower()):
                        missing.append("Requires %s, %s was found" %
                                       (req_lib, inst_lib))
                    break

            if not found:
                missing.append("Requires " + req_lib)

        return missing

    def _run_unzip(self, zip_dir, unzip_dir):
        cmd = "./nuage-unzip.sh %s %s" % (zip_dir, unzip_dir)
        self._print("Command: " + cmd)
        self._print("Unzipping %s to %s" % (zip_dir, unzip_dir))
        try:
            rc, output_lines = self._run_shell(cmd)
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("nuage-unzip.sh exit-code: %d" % rc)

            self._print("\nFiles unzipped successfully!")
        except Exception as e:
            self._print("\nAn error occurred while unzipping files: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)

    def _get_deployment_dir(self):
        if "deployment_dir" not in self.state:
            self._print("Creating a deployment file requires a deployment to"
                        " be specified.  This step will be skipped if not"
                        " provided.")
            choice = self._input("Do you want to specify a deployment now?", 0,
                                 ["(Y)es", "(n)o"])
            if choice != 1:
                self.create_deployment(None, None)

            if "deployment_dir" not in self.state:
                self._print("No deployment specified, skipping step")
                return None

        return self.state["deployment_dir"]

    def _read_deployment_file(self, deployment_file):
        with open(deployment_file, "r") as f:
            return yaml.safe_load(f.read().decode("utf-8"))

    def _setup_dns(self, deployment, data):
        self._print(self._get_field(data, "dns_setup_msg"))

        dns_domain_default = None
        if "dns_domain" in deployment:
            dns_domain_default = deployment["dns_domain"]

        dns_domain = self._input("Top level DNS domain?", dns_domain_default)
        deployment["dns_domain"] = dns_domain
        self.state["dns_domain"] = dns_domain

        if "vsd_fqdn_global" in deployment:
            vsd_fqdn_default = deployment["vsd_fqdn_global"]
        else:
            vsd_fqdn_default = "xmpp"

        self._print(self._get_field(data, "vsd_fqdn_msg"))

        vsd_fqdn = self._input("VSD FQDN (we'll add .%s)?" % dns_domain,
                               vsd_fqdn_default)

        if not vsd_fqdn.endswith(dns_domain):
            vsd_fqdn += "." + dns_domain

        deployment["vsd_fqdn_global"] = vsd_fqdn

        if "dns_server_list" in deployment:
            dns_servers_default = ",".join(deployment["dns_server_list"])
        else:
            dns_servers_default = None

        dns_server_list = self._input(
            "Enter DNS server IPs in dotted decmial format (separate multiple "
            "using commas)", dns_servers_default)

        deployment["dns_server_list"] = dns_server_list.split(",")

    def _setup_ntp(self, deployment, data):
        self._print(self._get_field(data, "ntp_setup_msg"))

        if "ntp_server_list" in deployment:
            ntp_servers_default = ",".join(deployment["ntp_server_list"])
        else:
            ntp_servers_default = None

        ntp_server_list = self._input(
            "Enter NTP server IPs in dotted decmial format (separate multiple "
            "using commas)", ntp_servers_default)

        deployment["ntp_server_list"] = ntp_server_list.split(",")


    def _generate_deployment_file(self, schema, output_file, deployment):
        # Import here because setup may not have been run at the start
        # up of the wizard and the library may not be present
        try:
            import jinja2
        except ImportError:
            self._print(
                "Cannot write deployment files because libraries are missing."
                "  Please make sure metro-setup.sh has been run.")
            return
        gen_example = ExampleFileGenerator(False, True)
        example_lines = gen_example.generate_example_from_schema(
            os.path.join("schemas", schema + ".json"))
        template = jinja2.Template(example_lines)
        rendered = template.render(**deployment)
        with open(output_file, 'w') as file:
            file.write(rendered.encode("utf-8"))


def main():
    try:
        wizard = Wizard()
        wizard()
    except Exception:
        traceback.print_exc()
        print "\nThere was an unexpected error running the wizard"
        print "Please contact: " + METROAE_CONTACT
        exit(1)


if __name__ == '__main__':
    main()
