#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import glob
import os
import re
import subprocess
import sys
import traceback

METROAE_CONTACT = "devops@nuagenetworks.net"

YAML_LIBRARY = "PyYAML==3.13"

WIZARD_SCRIPT = """

- message:
    text: |

      Thank you for using MetroAE!

      This wizard will walk you through the creation or modification
      of a MetroAE deployment. We will walk through the process
      step-by-step. You will also have the option of doing things
      such as verifying that all prerequisites are satisfied,
      unzipping Nuage image files, and copying ssh keys to servers.

      For assistance please contact: {contact}

- list_steps: {}
  description: |

      The following steps will be performed:

- step: Verify proper MetroAE installation
  description: |
      This step will verify that the MetroAE tool has been properly installed
      with all required libraries.
  verify_install:
    missing_msg: |

      We would like to run setup to install these.  The command is
      "sudo ./setup.sh" if you'd like to run it yourself.
      Running this command requires sudo access. You may be asked
      for the sudo password.
    wrong_os_msg: |

      The OS is not recognized.  MetroAE requires a Linux based operating
      system such as CentOS or Ubuntu.  A docker container version of MetroAE
      is available for other operating system types.

- step: Unzip image files
  description: |
      This step will unzip the image files needed for the VSP components.  The
      source zip files can be downloaded from Nokia OLCS:

      https://support.alcatel-lucent.com/portal/web/support

      For upgrade: Use the directory that contains the image files you are
      upgrading to.
  unzip_images:
    container_msg: |

      MetroAE is running in a container.  The zipped image files must be placed
      under the metroae_data directory mount point of the container.  The
      mount directory was set during container setup and can be found using
      the command "metroae container status".  Relative paths must be provided
      for both the source and destination directories that are relative to the
      metroae_data mount point.

- step: Create/read deployment
  description: |
      This step will create a deployment or modify an existing one.
      A deployment is a configuration set for MetroAE. It is a collection of
      files in a deployment directory. The name of the directory is the
      name of the deployment. The files in the directory describe the
      properties of each component being installed, upgraded, or configured.
      MetroAE supports multiple deployments, each in its own directory.
  create_deployment: {}

- step: Auto-discover existing components
  description: |
      This step can optionally attempt to discover components that are already
      running in your network.  By specifying the connection information of
      the hypervisors, any VMs running on these systems will be analyzed and
      entered as deployment data if identified as VSP components.  Any
      components sucessfully found in this way can be skipped in later steps.
  discover_components: {}

- step: Import CSV Spreadsheet
  description: |
      This step can optionally import MetroAE configuration via a CSV
      spreadsheet.  Any components defined in the spreadsheet can be skipped
      in the wizard.  A template for the spreadsheet can be found in the root
      MetroAE directory as "deployment_spreadsheet_template.csv".
  import_csv_spreadsheet: {}

- step: Common deployment parameters
  description: |
      This step will create or modify the common.yml file in your deployment.
      This file provides global parameters that are common to all components
      in your deployment.
  create_common:
    dns_setup_msg: |

      MetroAE requires that most components have hostname-to-ip address DNS
      mappings defined before running workflows. You can complete this
      wizard without having DNS setup in your environment, but having DNS
      setup before continuing will allow this wizard to auto-discover
      component IP addresses.
    vsd_fqdn_msg: |

      Please enter the Fully Qualified Domain Name (FQDN) for the VSD.  If
      clustered, use the XMPP FQDN. For standalone, use the FQDN of the VSD.
    ntp_setup_msg: |

      VSP components require the use of an NTP server so that components being
      installed/upgraded can keep their times synchronized.
    bridge_setup_msg: |

      Network bridges are required on vCenter and KVM target server
      hypervisors. A network bridge will be a Distributed Virtual PortGroup
      (DVPG) when deploying on vCenter or a Linux network bridge when deploying
      on KVM. VSP component interfaces will be connected to these bridges so
      that they can communicate with each other and to the outside.  MetroAE
      will not create the bridges for you. You must create and configure them
      ahead of time.

      There are up to three bridges that can be defined:

      mgmt_bridge: Management network.
      data_bridge: Internal data network.
      access_bridge: External network.

- step: Setup upgrade parameters
  description: |
      This step will create or modify the upgrade.yml file in your deployment.
      If you will not be doing an upgrade, this step can be skipped.
  create_upgrade:
    upgrade_msg: |

      MetroAE needs the version number that your deployment is currently
      running and which version to upgrade to.

- step: VSD deployment file
  description: |
      This step will create or modify the vsds.yml file in your deployment.
      This file provides parameters for the Virtualized Services Directories
      (VSDs) in your deployment. This step is only required if you are working
      with VSDs in your deployment.
  create_component:
    schema: vsds
    ha_amount: 3
    item_name: VSD
    upgrade_vmname: true

- step: VSC deployment file
  description: |
      This step will create or modify the vscs.yml file in your deployment.
      This file provides parameters for the Virtualized Services Controllers
      (VSCs) in your deployment. This step is only required if you are working
      with VSCs in your deployment.
  create_component:
    schema: vscs
    ha_amount: 2
    item_name: VSC
    upgrade_vmname: false

- step: VSTAT deployment file
  description: |
      This step will create or modify the vstats.yml file in your deployment.
      This file provides parameters for the VSD Statistics (Elasticsearch)
      nodes in your deployment. This step is only required if you are working
      with VSD Statistics nodes in your deployment.
  create_component:
    schema: vstats
    ha_amount: 3
    item_name: VSTAT
    upgrade_vmname: true

- step: NUH deployment file
  description: |
      This step will create or modify the nuhs.yml file in your deployment.
      This file provides parameters for the Nuage Utility Host VMs (NUHs) in
      your deployment.
  create_component:
    schema: nuhs
    ha_amount: 2
    item_name: NUH
    upgrade_vmname: false

- step: VNSUtil deployment file
  description: |
      This step will create or modify the vnsutils.yml file in your deployment.
      This file provides parameters for the VNS utility VM (Proxy) nodes
      in your deployment. This step is only required if you wish to deploy a
      VNS setup.
  create_component:
    schema: vnsutils
    ha_amount: any
    item_name: VNSUtil
    upgrade_vmname: false

- step: NSGvs deployment file
  description: |
      This step will create or modify the nsgvs.yml file in your deployment.
      This file provides parameters for the virtualized Network Service Gateway
      (NSGv) nodes in your deployment. This step is only required if you wish
      to deploy a VNS setup.
  create_component:
    schema: nsgvs
    ha_amount: any
    item_name: NSGv
    upgrade_vmname: false

- step: NSGv bootstrap deployment file
  description: |
      This step will create or modify the nsgv_bootstrap.yml file in your
      deployment.  This file provides the global parameters for bootstrapping
      your NSGv nodes.  This step is only required if you wish
      to deploy a VNS setup and you are using metro to perform a zero-factor
      bootstrap.
  create_bootstrap: {}

- step: Setup SSH on target servers
  description: |
      This step will setup password-less SSH access to the KVM target servers
      (hypervisors) used by your deployment.  MetroAE must have password-less
      access to all the KVM target servers you will be accessing using this
      deployment. If you are not using KVM target servers you may skip this
      step.
  setup_target_servers:
    container_msg: |

      MetroAE is running in a container.  The SSH key being copied to the
      target servers is the key belonging to the container.  This is different
      than the key on the Docker host.  The container SSH key can be found in
      your metroae_data mount directory.

- complete_wizard:
    problem_msg: |

        The following problems have occurred during the wizard.  It may
        cause MetroAE to function incorrectly.  It is recommended that you
        correct these and repeat any steps affected.
    finish_msg: |

        All steps of the wizard have been performed.  You can use (b)ack to
        repeat previous steps or (q)uit to exit the wizard.
    complete_msg: |

      The wizard is complete!
    install_msg: |
        You can issue the following to begin installing your components:

        {metro} install everything {deployment}
    upgrade_msg: |
        You can issue the following to begin an upgrade of your components:

        {metro} upgrade everything {deployment}

"""

STANDARD_FIELDS = ["step", "description"]
TARGET_SERVER_TYPE_LABELS = ["(K)vm", "(v)center", "(o)penstack", "(a)ws"]
TARGET_SERVER_TYPE_VALUES = ["kvm", "vcenter", "openstack", "aws"]

COMPONENT_LABELS = ["vs(d)", "vs(c)", "(e)s", "nu(h)", "vns(u)tils", "ns(g)v",
                    "(n)one of these - skip VM"]
COMPONENT_DEFAULT_LABELS = ["vs(D)", "vs(C)", "(E)s", "nu(H)", "vns(U)tils",
                            "ns(G)v", "(N)one of these - skip VM"]
COMPONENT_IMAGE_KEYWORDS = ["vsd", "vsc", "elastic", "nuage-utils", "vns-util",
                            "ncpe"]
COMPONENT_SCHEMAS = ["vsds", "vscs", "vstats", "nuhs", "vnsutils", "nsgvs"]


class Wizard(object):

    def __init__(self, script=WIZARD_SCRIPT):
        self._set_container()
        self._set_directories()
        self.state = dict()
        self.current_action_idx = 0
        self.progress_display_count = 0
        self.progress_display_rate = 1

        if "NON_INTERACTIVE" in os.environ:
            self.args = list(sys.argv)
            self.args.pop(0)
        else:
            self.args = list()

        self._import_yaml()
        import yaml
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
        self._print(u"\nVerifying MetroAE installation")

        if self.in_container:
            self._print("\nWizard is being run inside a Docker container.  "
                        "No need to verify installation.  Skipping step...")
            return

        if not os.path.isfile("/etc/os-release"):
            self._record_problem("wrong_os", "Unsupported operating system")
            self._print(self._get_field(data, "wrong_os_msg"))

            choice = self._input("Do you wish to continue anyway?", 0,
                                 ["(Y)es", "(n)o"])

            if choice == 1:
                self._print("Quitting wizard...")
                exit(0)

        missing = self._verify_pip()
        yum_missing = self._verify_yum()

        missing.extend(yum_missing)

        if len(missing) == 0:
            self._unrecord_problem("install_libraries")
            self._print(u"\nMetroAE Installation OK!")
        else:
            self._record_problem(
                "install_libraries",
                u"Your MetroAE installation is missing libraries")
            self._print(u"\nYour MetroAE installation is missing libraries:\n")
            self._print("\n".join(missing))
            self._print(self._get_field(data, "missing_msg"))
            choice = self._input("Do you want to run setup now?", 0,
                                 ["(Y)es", "(n)o"])

            if choice != 1:
                self._run_setup()

    def unzip_images(self, action, data):
        valid = False
        while not valid:
            if self.in_container:
                self._print(self._get_field(data, "container_msg"))
                zip_dir = self._input("Please enter the directory relative to "
                                      "the metroae_data mount point that "
                                      "contains your zip files", "")

                if zip_dir.startswith("/"):
                    self._print("\nDirectory must be a relative path.")
                    continue

                full_zip_dir = os.path.join("/metroae_data", zip_dir)

            else:
                zip_dir = self._input("Please enter the directory that "
                                      "contains your zip files", "")
                full_zip_dir = zip_dir

            if zip_dir == "" or not os.path.exists(full_zip_dir):
                choice = self._input(
                    "Directory not found. Would you like to skip unzipping",
                    0, ["(Y)es", "(n)o"])
                if choice != 1:
                    self._print("Skipping unzip step...")
                    return
            elif not os.path.isdir(full_zip_dir):
                self._print("%s is not a directory, please enter the directory"
                            " containing the zipped files" % zip_dir)
            else:
                valid = True

        if self.in_container:
            valid = False
            while not valid:
                unzip_dir = self._input("Please enter the directory relative "
                                        "to the metroae_data mount point to "
                                        "unzip to")
                if unzip_dir.startswith("/"):
                    self._print("\nDirectory must be a relative path.")
                else:
                    valid = True

            full_unzip_dir = os.path.join("/metroae_data", unzip_dir)
        else:
            unzip_dir = self._input("Please enter the directory to unzip to")
            full_unzip_dir = unzip_dir

        self.state["nuage_unzipped_files_dir"] = unzip_dir

        choice = self._input(
            "Unzip %s to %s" % (zip_dir, unzip_dir),
            0, ["(Y)es", "(n)o"])
        if choice == 0:
            self._run_unzip(full_zip_dir, full_unzip_dir)
        else:
            self._print("Skipping unzip step...")

    def create_deployment(self, action, data):
        valid = False
        while not valid:
            deployment_name = self._input(
                "Please enter the name of the deployment (will be the "
                "directory name)", "default")
            if "/" in deployment_name:
                self._print("\nA deployment name cannot contain a slash "
                            "because it will be a directory name")
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
        deployment_dir = os.path.join(self.base_deployment_path,
                                      deployment_name)
        if os.path.isdir(deployment_dir):
            self._print("\nThe deployment directory was found")
            found = True
        else:
            self._print("")
            choice = self._input('Create deployment directory: "%s"?' %
                                 deployment_name,
                                 0, ["(Y)es", "(n)o"])
            if choice == 1:
                self._print("Skipping deployment creation.")
                return

        self._print("Deployment directory: " + deployment_dir)
        self.state["deployment_name"] = deployment_name
        self.state["deployment_dir"] = deployment_dir

        if not found:
            os.mkdir(deployment_dir)

    def discover_components(self, action, data):
        choice = 0
        another_string = "a"

        while choice == 0:
            choice = self._input(
                "Would you like to try to discover existing components "
                "automatically from %s hypervisor?" % another_string, 1,
                ["(y)es", "(N)o"])

            if choice == 1:
                return

            self._discover_components()
            another_string = "another"

    def import_csv_spreadsheet(self, action, data):
        choice = self._input("Do you have a CSV spreadsheet to import?", 1,
                             ["(y)es", "(N)o"])

        if choice == 1:
            return

        self._import_csv()

    def create_common(self, action, data):

        if self._check_skip_for_csv("common"):
            return

        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        deployment_file = os.path.join(deployment_dir, "common.yml")
        if os.path.isfile(deployment_file):
            deployment = self._read_deployment_file(deployment_file,
                                                    is_list=False)
        else:
            self._print(deployment_file + " not found. It will be created.")
            deployment = dict()

        self._setup_unzip_dir(deployment)

        self._setup_target_server_type()

        if self.state["target_server_type"] == "kvm":
            self._setup_bridges(deployment, data)
        elif self.state["target_server_type"] == "vcenter":
            self._setup_vcenter(deployment)

        self._setup_dns(deployment, data)

        self._setup_ntp(deployment, data)

        default = self._get_value(deployment, "vsd_license_file")
        if default is None:
            default = ""
        license = self._input("Path to VSD License file (required only for "
                              "NSGv bootstrapping)", default)
        if license != "":
            deployment["vsd_license_file"] = license

        self._generate_deployment_file("common", deployment_file, deployment)

    def create_upgrade(self, action, data):
        if self._check_skip_for_csv("upgrade"):
            return

        self._print("")
        choice = self._input("Will you be performing an upgrade?", 0,
                             ["(Y)es", "(N)o"])
        if choice == 1:
            if "upgrade" in self.state:
                del self.state["upgrade"]
            self._print("Skipping step...")
            return

        self.state["upgrade"] = True

        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        deployment_file = os.path.join(deployment_dir, "upgrade.yml")
        if os.path.isfile(deployment_file):
            deployment = self._read_deployment_file(deployment_file,
                                                    is_list=False)
        else:
            self._print(deployment_file + " not found. It will be created.")
            deployment = dict()

        self._setup_upgrade(deployment, data)

        self._generate_deployment_file("upgrade", deployment_file, deployment)

    def create_component(self, action, data):
        schema = self._get_field(data, "schema")
        item_name = self._get_field(data, "item_name")
        is_vsc = (schema == "vscs")
        is_nuh = (schema == "nuhs")
        is_nsgv = (schema == "nsgvs")
        is_vnsutil = (schema == "vnsutils")

        if self._check_skip_for_csv(schema):
            return

        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        deployment_file = os.path.join(deployment_dir, schema + ".yml")
        if os.path.isfile(deployment_file):
            deployment = self._read_deployment_file(deployment_file,
                                                    is_list=True)
        else:
            self._print(deployment_file + " not found. It will be created.")
            deployment = list()

        self._setup_target_server_type()

        self._print("\nPlease enter your %s deployment type\n" % item_name)

        amount = self._get_number_components(deployment, data)
        deployment = deployment[0:amount]

        if not is_nsgv:
            self._print("\nIf DNS is configured properly, IP addresses can be "
                        "auto-discovered.")

        for i in range(amount):
            self._print("\n%s %d\n" % (item_name, i + 1))
            if len(deployment) == i:
                deployment.append(dict())

            deployment[i]["target_server_type"] = (
                self.state["target_server_type"])

            if is_nsgv:
                hostname = "nsgv" + str(i + 1)
            else:
                hostname = self._setup_hostname(deployment, i, item_name)

            if is_nsgv or is_vnsutil:
                with_upgrade = False
            else:
                with_upgrade = (self._get_field(data, "upgrade_vmname") and
                                "upgrade" in self.state)

            if not is_nuh:
                self._setup_vmname(deployment, i, hostname, with_upgrade)

            if not is_nsgv:
                self._setup_ip_addresses(deployment, i, hostname, is_vsc)
            else:
                component = deployment[i]
                self._setup_target_server(component)
                self._setup_nsgv_component(component)

            if is_vnsutil:
                component = deployment[i]
                self._setup_vnsutils(component, i)

        if amount == 0:
            if os.path.isfile(deployment_file):
                os.remove(deployment_file)
        else:
            self._generate_deployment_file(schema, deployment_file, deployment)

    def create_bootstrap(self, action, data):
        if self._check_skip_for_csv("nsgv_bootstrap"):
            return

        self._print("")
        if "metro_bootstrap" not in self.state:
            choice = self._input("Will you be using metro to bootstrap NSGvs?",
                                 1, ["(y)es", "(N)o"])
            if choice == 1:
                self._print("Skipping step...")
                return

        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        deployment_file = os.path.join(deployment_dir, "nsgv_bootstrap.yml")
        if os.path.isfile(deployment_file):
            deployment = self._read_deployment_file(deployment_file,
                                                    is_list=False)
        else:
            self._print(deployment_file + " not found. It will be created.")
            deployment = dict()

        self._setup_bootstrap(deployment, data)

        self._generate_deployment_file("nsgv_bootstrap", deployment_file,
                                       deployment)

    def setup_target_servers(self, action, data):

        if "all_target_servers" in self.state:
            servers = self.state["all_target_servers"]
        else:
            servers = None
            while servers is None:
                servers = self._input(
                    "Enter target server (hypervisor) addresses (separate "
                    "multiple using commas)")
                servers = self._format_ip_list(servers)
                servers = self._validate_hostname_list(servers)

            self.state["all_target_servers"] = servers

        if "target_server_username" in self.state:
            default = self.state["target_server_username"]
        else:
            default = "root"

        username = self._input(
            "Enter the username for the target servers (hypervisors)", default)
        self.state["target_server_username"] = username

        self._print("\nWe will now configure SSH access to the target servers"
                    " (hypervisors).  This will likely require the SSH"
                    " password for each system would need to be entered.")

        if self.in_container:
            self._print(self._get_field(data, "container_msg"))

        choice = self._input("Setup SSH now?", 0, ["(Y)es", "(n)o"])

        if choice == 1:
            self._print("Skipping step...")
            return

        for server in servers:
            self._setup_ssh(username, server)

        choice = self._input("Verify SSH connectivity now?", 0,
                             ["(Y)es", "(n)o"])

        if choice == 1:
            return

        for server in servers:
            valid = self._verify_ssh(username, server)
            if valid and "mgmt_bridge" in self.state:
                valid = self._verify_bridge(username, server,
                                            self.state["mgmt_bridge"])
            if valid and "data_bridge" in self.state:
                valid = self._verify_bridge(username, server,
                                            self.state["data_bridge"])
            if valid and "access_bridge" in self.state:
                valid = self._verify_bridge(username, server,
                                            self.state["access_bridge"])

    def complete_wizard(self, action, data):
        if self._has_problems():
            self._print(self._get_field(data, "problem_msg"))
            self._list_problems()

        self._print(self._get_field(data, "finish_msg"))
        choice = self._input(None, None, ["(q)uit", "(b)ack"])

        if choice == 1:
            self.current_action_idx -= 2
            return
        else:
            self._print(self._get_field(data, "complete_msg"))
            metro = "./metroae"
            if self.in_container:
                metro = "metroae"

            deployment = ""
            if ("deployment_name" in self.state and
                    self.state["deployment_name"] != "default"):
                deployment = self.state["deployment_name"]
            if "upgrade" in self.state:
                self._print(
                    self._get_field(data, "upgrade_msg").format(
                        metro=metro,
                        deployment=deployment))
            else:
                self._print(
                    self._get_field(data, "install_msg").format(
                        metro=metro,
                        deployment=deployment))
            exit(0)

    #
    # Private class internals
    #

    def _print(self, msg):
        print msg.encode("utf-8")

    def _print_progress(self):
        if self.progress_display_count % self.progress_display_rate == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        self.progress_display_count += 1

    def _input(self, prompt=None, default=None, choices=None, datatype=""):
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
                                         choices, datatype)
            if value is None:
                raise Exception("Invalid non-interactive input for %s%s" %
                                (input_prompt, user_value))

        else:
            while value is None:
                if datatype == "password":
                    user_value = getpass.getpass(input_prompt)
                else:
                    user_value = raw_input(input_prompt)
                value = self._validate_input(user_value, default, choices,
                                             datatype)

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

    def _validate_input(self, user_value, default=None, choices=None,
                        datatype=""):
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
        elif datatype == "ipaddr":
            value = self._validate_ipaddr(user_value)
            if value is None:
                self._print("\nValue is not a valid ipaddress\n")
        elif datatype == "int":
            try:
                value = int(user_value)
            except ValueError:
                self._print("\nValue is not a valid integer\n")
                return None
        elif datatype == "hostname":
            value = self._validate_hostname(user_value)
            if value is None:
                self._print("\nValue is not a valid hostname\n")
        elif datatype == "version":
            allowed = re.compile("^[\d][.][\d][.]([A-Z\d]+)$", re.IGNORECASE)
            if not allowed.match(user_value):
                self._print("\nValue is not a valid version\n")
                return None
            value = user_value
        else:
            value = user_value

        return value

    def _validate_ipaddr(self, user_value):
        try:
            import netaddr
            try:
                netaddr.IPAddress(user_value)
                return user_value
            except netaddr.core.AddrFormatError:
                return None
        except ImportError:
            self._print("\nWarning: Python netaddr library not installed. "
                        "Cannot validate IP address.  This library is also "
                        "required for MetroAE to run properly.")
            return user_value

    def _validate_hostname(self, hostname):
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if all(allowed.match(x) for x in hostname.split(".")):
            return hostname
        else:
            return None

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

    def _import_yaml(self):
        try:
            import yaml
            yaml.safe_load("")
        except ImportError:
            self._install_yaml()

    def _install_yaml(self):
        self._print("This wizard requires PyYAML library to be installed."
                    "  Running this command requires sudo access.  You may be "
                    "asked for the sudo password.\n")
        choice = self._input("Install it now?", 0,
                             ["(Y)es", "(n)o"])
        if choice == 1:
            self._print("Please install PyYAML and run the wizard again.")
            exit(1)

        rc, output_lines = self._run_shell("sudo pip install " + YAML_LIBRARY)
        if rc != 0:
            self._print("\n".join(output_lines))
            self._print("Could not install PyYAML, exit code: %d" % rc)
            self._print("Please install PyYAML and run the wizard again.")
            exit(1)

    def _get_value(self, deployment, field):
        value = deployment.get(field)
        if value == "":
            value = None
        return value

    def _set_container(self):
        # For Dalston container
        if "RUN_MODE" in os.environ:
            self.in_container = (os.environ["RUN_MODE"] == "INSIDE")
        else:
            self.in_container = False
        self.in_container = os.path.isdir("/source/nuage-metro")

    def _set_directories(self):
        self.metro_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.metro_path)
        if self.in_container:
            self.base_deployment_path = os.path.join("/data",
                                                     "deployments")
            # Dalston container
            self.base_deployment_path = os.path.join("/metroae_data",
                                                     "deployments")
        else:
            self.base_deployment_path = os.path.join(self.metro_path,
                                                     "deployments")

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
        self.current_action_idx = 0

        while self.current_action_idx < len(self.script):
            current_action = self.script[self.current_action_idx]
            if "step" in current_action:
                self._display_step(current_action)
                choice = self._input(None, 0, ["(C)ontinue",
                                               "(b)ack",
                                               "(s)kip",
                                               "(q)uit"])
                if choice == 1:
                    self.current_action_idx -= 1
                    continue
                if choice == 2:
                    self.current_action_idx += 1
                    continue
                if choice == 3:
                    self._print("Exiting MetroAE wizard. All progress made "
                                "has been saved.")
                    exit(0)

            try:
                self._run_action(current_action)
            except KeyboardInterrupt:
                self._print("\n\nInterrupt signal received. All progress made "
                            "before current step has been saved.\n")
                choice = self._input(
                    "Would you like to quit?",
                    1, ["(y)es", "(N)o"])

                if choice != 1:
                    exit(1)

            self.current_action_idx += 1

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
                                   cwd=self.metro_path,
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
                if "DEBUG_WIZARD" in os.environ:
                    self._print(line)
                else:
                    self._print_progress()
            else:
                # Flush stdout buffer
                lines = process.stdout.read()
                for line in lines.split("\n"):
                    output_lines.append(line)
                    if "DEBUG_WIZARD" in os.environ:
                        self._print(line)
                    else:
                        self._print_progress()
                return retcode

    def _record_problem(self, problem_name, problem_descr):
        if "problems" not in self.state:
            self.state["problems"] = dict()

        self.state["problems"][problem_name] = problem_descr

    def _unrecord_problem(self, problem_name):
        if "problems" not in self.state:
            return

        if problem_name in self.state["problems"]:
            del self.state["problems"][problem_name]

    def _has_problems(self):
        return "problems" in self.state and len(self.state["problems"]) != 0

    def _list_problems(self):
        if self._has_problems():
            for descr in self.state["problems"].values():
                self._print(" - " + descr)

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
        cmd = "sudo ./setup.sh"
        self._print("Command: " + cmd)
        self._print("Running setup (may ask for sudo password)")
        try:
            rc, output_lines = self._run_shell(cmd)
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("setup.sh exit-code: %d" % rc)

            self._unrecord_problem("install_libraries")
            self._print(u"\nMetroAE setup completed successfully!")
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
        self._print("Unzipping files from %s to %s" % (zip_dir, unzip_dir))
        for f in glob.glob(os.path.join(zip_dir, "*.gz")):
            self._print(f)
        try:
            rc, output_lines = self._run_shell(cmd)
            if rc != 0:
                self._record_problem(
                    "unzip_files", "Unable to unzip files")
                self._print("\n".join(output_lines))
                raise Exception("nuage-unzip.sh exit-code: %d" % rc)

            self._unrecord_problem("unzip_files")
            self._print("\nFiles unzipped successfully!")
        except Exception as e:
            self._record_problem(
                "unzip_files", "Error occurred while unzipping files")
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

    def _read_deployment_file(self, deployment_file, is_list):
        with open(deployment_file, "r") as f:
            import yaml
            deployment = yaml.safe_load(f.read().decode("utf-8"))
            if is_list and type(deployment) != list:
                deployment = list()
            if not is_list and type(deployment) != dict:
                deployment = dict()
            return deployment

    def _discover_components(self):
        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        hostname = self._input("Enter target server (hypervisor) address")
        if self._verify_vcenter_hypervisor(hostname):
            username = self._input(
                "Enter the username for the target server (hypervisor)",
                "Administrator@vsphere.local")
            password = self._input(
                "Enter the password for the target server",
                datatype="password")
            self._discover_vcenter_components(username, password, hostname)
        else:
            username = self._input(
                "Enter the username for the target server (hypervisor)",
                "root")

            valid_ssh = self._setup_discovery_ssh(username, hostname)

            if not valid_ssh:
                self._print("Auto-discovery requires password-less SSH access")
                return

            if self._verify_kvm_hypervisor(username, hostname):
                self._discover_kvm_components(username, hostname)
            else:
                self._print("Unsupported hypervisor type for auto-discovery "
                            "(only KVM and vCenter supported)")
                return

    def _setup_discovery_ssh(self, username, hostname):
        valid_ssh = self._verify_ssh(username, hostname)

        if valid_ssh:
            return valid_ssh

        choice = self._input(
            "Add password-less SSH access to %s?" % hostname, 0,
            ["(Y)es", "(n)o"])

        if choice != 0:
            return False

        self._print("\nWe will now configure SSH access to the target "
                    "server (hypervisors).  This will likely require the "
                    "SSH password to be entered.\n")

        valid_ssh = self._setup_ssh(username, hostname)

        return valid_ssh

    def _verify_vcenter_hypervisor(self, hostname):
        # TODO
        return True

    def _verify_kvm_hypervisor(self, username, hostname):
        try:
            rc, output_lines = self._run_on_hypervisor(
                username, hostname,
                "ps ax | grep libvirtd | grep -v grep")

            return rc == 0
        except Exception:
            self._print("Could not connect to hypervisor")
            pass

        return False

    def _discover_vcenter_components(self, username, password, hostname):
        try:
            vms = self._get_vcenter_vms(username, password, hostname)
            if vms is None:
                return False

            self._print("\nFound VMs: " + ", ".join(sorted(vms.keys())))

            for vm_name, vm in vms.iteritems():
                vm_info = self._discover_vcenter_vm_info(vm, hostname)
                if vm_info is not None:
                    choice = self._verify_vcenter_discovery(vm_info)
                    try:
                        self._add_discovered_vm(vm_info, choice)
                    except Exception:
                        self._print("\nCould not add VM to deployment.")
            return True

        except Exception as e:
            self._print("\nAn error occurred while attempting to auto-discover"
                        " components: " + str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return False

    def _get_vcenter_vms(self, username, password, hostname):
        try:
            from pyVim.connect import SmartConnectNoSSL, Disconnect
            from pyVmomi import vim
            import ssl
            import atexit
        except ImportError:
            self._print("Could not import libraries required to communicate "
                        "with vCenter. Was setup completed successfully?")
            return None

        try:
            s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            s.verify_mode = ssl.CERT_NONE
            si = SmartConnectNoSSL(host=hostname,
                                   user=username,
                                   pwd=password)
            atexit.register(Disconnect, si)

        except Exception:
            self._print("Could not connect to vCenter")
            return None

        return self._get_vcenter_vms_dict(si.content, [vim.VirtualMachine])

    def _get_vcenter_vms_dict(self, connection, vimtype):
        vms_dict = {}
        container = connection.viewManager.CreateContainerView(
            connection.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
            vms_dict.update({managed_object_ref.name: managed_object_ref})

        return vms_dict

    def _discover_vcenter_vm_info(self, vm, hostname):
        try:
            vm_info = dict()

            vm_info["vm_name"] = vm.name
            vm_info["target_server"] = hostname
            vm_info["target_server_type"] = "vcenter"

            self._discover_vcenter_vm_field(
                vm_info, vm, "product",
                lambda vm: vm.summary.config.product.name)

            self._discover_vcenter_vm_field(
                vm_info, vm, "datacenter",
                lambda vm: vm.summary.runtime.host.parent.parent.parent.name)

            self._discover_vcenter_vm_field(
                vm_info, vm, "cluster",
                lambda vm: vm.summary.runtime.host.parent.name)

            self._discover_vcenter_vm_field(
                vm_info, vm, "datastore",
                lambda vm: vm.config.datastoreUrl[0].name)

            interfaces = list()
            vm_info["interfaces"] = interfaces

            self._discover_vcenter_interfaces(interfaces, vm)

            return vm_info

        except Exception:
            return None

    def _discover_vcenter_vm_field(self, vm_info, vm, field, get_callback):
        vm_info[field] = ''
        try:
            vm_info[field] = get_callback(vm)
        except Exception:
            pass

    def _discover_vcenter_interfaces(self, interfaces, vm):
        try:
            if len(vm.guest.net) > 0:
                interface = dict()
                interfaces.append(interface)

                self._discover_vcenter_vm_field(
                    interface, vm, "address",
                    lambda vm: vm.guest.net[0].ipAddress[0])

                self._discover_vcenter_vm_field(
                    interface, vm, "hostname",
                    lambda vm: vm.guest.ipStack[0].dnsConfig.hostName)

                self._discover_vcenter_vm_field(
                    interface, vm, "gateway",
                    lambda vm: vm.guest.ipStack[0].ipRouteConfig
                    .ipRoute[0].gateway.ipAddress)

                self._discover_vcenter_vm_field(
                    interface, vm, "prefix",
                    lambda vm: vm.guest.net[0].ipConfig.ipAddress[0]
                    .prefixLength)

                if interface['prefix'] == '':
                    interface['prefix'] = 24

            if len(vm.guest.net) > 1:
                interface = dict()
                interfaces.append(interface)

                self._discover_vcenter_vm_field(
                    interface, vm, "address",
                    lambda vm: vm.guest.net[1].ipAddress[0])

                interface['hostname'] = ""
                interface['gateway'] = ""
                interface['prefix'] = 24

        except Exception:
            pass

    def _verify_vcenter_discovery(self, vm_info):
        self._print("\n\nDiscovered VM")
        self._print("-------------")
        self._print("VM name: " + vm_info["vm_name"])
        self._print("Product: " + vm_info["product"])
        self._print("Datacenter: " + vm_info["datacenter"])
        self._print("Cluster: " + vm_info["cluster"])
        self._print("Datastore: " + vm_info["datastore"])
        self._print("Interfaces:")
        for interface in vm_info["interfaces"]:
            self._print(" - address: " + interface["address"])
            self._print("   hostname: " + interface["hostname"])
            self._print("   gateway: " + interface["gateway"])
            self._print("   prefix length: " + str(interface["prefix"]))

        self._print("\nThis VM can be added to your deployment.  There will be"
                    " an opportunity to modify it in later steps of the wizard"
                    " or those steps can be skipped if the discovered VMs are "
                    "correct.\n")
        return self._vcenter_component_choice(vm_info["product"])

    def _vcenter_component_choice(self, product):

        default = len(COMPONENT_LABELS) - 1
        if "vsc" in product.lower():
            default = 1

        choices = list(COMPONENT_LABELS)
        choices[default] = COMPONENT_DEFAULT_LABELS[default]
        choice = self._input("Which component type is this VM?", default,
                             choices)

        return choice

    def _discover_kvm_components(self, username, hostname):
        try:
            vm_names = self._discover_kvm_vm_names(username, hostname)
            for vm_name in vm_names:
                vm_info = self._discover_kvm_vm_info(username, hostname,
                                                     vm_name)
                if vm_info is not None:
                    choice = self._verify_kvm_discovery(vm_info)
                    try:
                        self._add_discovered_vm(vm_info, choice)
                    except Exception:
                        self._print("\nCould not add VM to deployment.")
            return True
        except Exception as e:
            self._print("\nAn error occurred while attempting to auto-discover"
                        " components: " + str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return False

    def _discover_kvm_vm_names(self, username, hostname):
        rc, output_lines = self._run_on_hypervisor(username, hostname,
                                                   "sudo virsh list --name")
        if rc == 0:
            names = sorted([x for x in output_lines if x.strip() != ""])
            self._print("\nFound VMs: " + ", ".join(names))
            return names
        else:
            self._print("\nError while discovering VMs on %s\n%s" % (
                hostname, "\n".join(output_lines)))
            return list()

    def _discover_kvm_vm_info(self, username, hostname, vm_name):
        rc, output_lines = self._run_on_hypervisor(
            username, hostname, "sudo virsh dumpxml " + vm_name)

        if rc != 0:
            return None

        vm_info = self._parse_kvm_info("\n".join(output_lines))

        if vm_info is None:
            return None

        vm_info["target_server"] = hostname
        vm_info["target_server_type"] = "kvm"
        vm_info["vm_name"] = vm_name

        for interface in vm_info["interfaces"]:
            self._discover_kvm_interface(username, hostname, interface)

        return vm_info

    def _parse_kvm_info(self, kvm_xml):
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            self._print(
                "Could not import the libraries to parse KVM XML. Discovery "
                "not possible.")
            return None

        vm_info = dict()
        try:
            root = ET.fromstring(kvm_xml)

            vm_info["image_name"] = (
                root.find("devices/disk/source").attrib["file"])

            interfaces = list()

            vm_info["interfaces"] = interfaces

            for intf_elem in root.findall("devices/interface[@type='bridge']"):
                interfaces.append({
                    "mac": intf_elem.find("mac").attrib["address"],
                    "bridge": intf_elem.find("source").attrib["bridge"]})

            return vm_info

        except Exception:
            self._print(
                "Could not parse KVM XML. Skipping VM.")
            return None

    def _discover_kvm_interface(self, username, hostname, interface):
        interface["address"] = ""
        try:
            rc, output_lines = self._run_on_hypervisor(
                username, hostname,
                "/usr/sbin/arp -en | grep " + interface["mac"])
            if rc == 0:
                interface["address"] = output_lines[0].split(" ")[0]

        except Exception:
            pass

        interface["hostname"] = ""
        try:
            if interface["address"] != "":
                rc, output_lines = self._run_on_hypervisor(
                    username, hostname,
                    "getent hosts " + interface["address"])
                if rc == 0:
                    interface["hostname"] = output_lines[0].split(" ")[-1]
        except Exception:
            pass

        interface["gateway"] = ""
        interface["prefix"] = 24
        try:
            if interface["address"] != "":
                rc, output_lines = self._run_on_hypervisor(
                    username, hostname,
                    "/usr/sbin/ip address show dev %s | "
                    "awk '/inet/ {print $2}'" % interface["bridge"])
                if rc == 0:
                    interface["gateway"] = output_lines[0].split("/")[0]
                    interface["prefix"] = int(output_lines[0].split("/")[1])
        except Exception:
            pass

    def _verify_kvm_discovery(self, vm_info):
        self._print("\n\nDiscovered VM")
        self._print("-------------")
        self._print("VM name: " + vm_info["vm_name"])
        self._print("Image: " + vm_info["image_name"])
        self._print("Interfaces:")
        for interface in vm_info["interfaces"]:
            self._print(" - bridge: " + interface["bridge"])
            self._print("   address: " + interface["address"])
            self._print("   hostname: " + interface["hostname"])
            self._print("   gateway: " + interface["gateway"])
            self._print("   prefix length: " + str(interface["prefix"]))

        self._print("\nThis VM can be added to your deployment.  There will be"
                    " an opportunity to modify it in later steps of the wizard"
                    " or those steps can be skipped if the discovered VMs are "
                    "correct.\n")
        return self._kvm_component_choice(vm_info["image_name"])

    def _kvm_component_choice(self, image_name):

        default = len(COMPONENT_IMAGE_KEYWORDS)
        for i, keyword in enumerate(COMPONENT_IMAGE_KEYWORDS):
            if keyword in image_name.lower():
                default = i

        choices = list(COMPONENT_LABELS)
        choices[default] = COMPONENT_DEFAULT_LABELS[default]
        choice = self._input("Which component type is this VM?", default,
                             choices)

        return choice

    def _add_discovered_vm(self, vm_info, choice):

        if choice >= len(COMPONENT_LABELS) - 1:
            # Skip
            return

        schema = COMPONENT_SCHEMAS[choice]
        if "discovered_" + schema in self.state:
            deployment = self.state["discovered_" + schema]
        else:
            deployment = list()
            self.state["discovered_" + schema] = deployment

        component = dict()
        self._add_discovered_vm_standard(vm_info, component)
        role = 1
        if choice == 0:
            role = self._input("Role of VSD?", 0, [
                "(P)rimary / stand-alone",
                "(s)tandby"])
        if role == 0:
            deployment.insert(0, component)
        else:
            deployment.append(component)

        if choice == 0:
            # VSD
            pass
        elif choice == 1:
            # VSC
            self._add_discovered_vm_vsc(vm_info, component)
        elif choice == 2:
            # VSTAT
            pass
        elif choice == 3:
            # NUH
            pass
        elif choice == 4:
            # VNSUTIL
            self._add_discovered_vm_vnsutil(vm_info, component)
        elif choice == 5:
            # NSG
            self._add_discovered_vm_nsgv(vm_info, component)
        else:
            # UNKNOWN
            self._print("\nError: Unknown choice for discovered VM\n")
            return

        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return
        deployment_file = os.path.join(deployment_dir, schema + ".yml")
        self._generate_deployment_file(schema, deployment_file, deployment)

    def _add_discovered_vm_standard(self, vm_info, component):
        component["target_server_type"] = vm_info["target_server_type"]
        component["target_server"] = vm_info["target_server"]
        component["vmname"] = vm_info["vm_name"]
        component["upgrade_vmname"] = "new-" + vm_info["vm_name"]

        if "datacenter" in vm_info and vm_info["datacenter"] != "":
            component["vcenter_datacenter"] = vm_info["datacenter"]

        if "cluster" in vm_info and vm_info["cluster"] != "":
            component["vcenter_cluster"] = vm_info["cluster"]

        if "datastore" in vm_info and vm_info["datastore"] != "":
            component["vcenter_datastore"] = vm_info["datastore"]

        if "interfaces" in vm_info and len(vm_info["interfaces"]) > 0:
            first_interface = vm_info["interfaces"][0]
            component["hostname"] = first_interface["hostname"]
            component["mgmt_ip"] = first_interface["address"]
            component["mgmt_ip_prefix"] = first_interface["prefix"]
            component["mgmt_gateway"] = first_interface["gateway"]
            if "bridge" in first_interface:
                component["mgmt_bridge"] = first_interface["bridge"]

    def _add_discovered_vm_vsc(self, vm_info, component):
        if "interfaces" in vm_info and len(vm_info["interfaces"]) > 1:
            second_interface = vm_info["interfaces"][1]
            component["ctrl_ip"] = second_interface["address"]
            component["ctrl_ip_prefix"] = second_interface["prefix"]
            if "bridge" in second_interface:
                component["data_bridge"] = second_interface["bridge"]

        system_ip = self._input("System IP address for routing", None,
                                datatype="ipaddr")
        component["system_ip"] = system_ip

    def _add_discovered_vm_vnsutil(self, vm_info, component):
        if "interfaces" in vm_info and len(vm_info["interfaces"]) > 1:
            second_interface = vm_info["interfaces"][1]
            component["data_ip"] = second_interface["address"]
            component["data_ip_prefix"] = second_interface["prefix"]
            if "bridge" in second_interface:
                component["data_bridge"] = second_interface["bridge"]

        self._setup_vnsutils(component, 0)

    def _add_discovered_vm_nsgv(self, vm_info, component):
        del component["mgmt_bridge"]
        if "interfaces" in vm_info and len(vm_info["interfaces"]) > 0:
            first_interface = vm_info["interfaces"][0]
            component["nsgv_ip"] = first_interface["address"]
            if "mac" in first_interface:
                component["nsgv_mac"] = first_interface["mac"]
            if "bridge" in first_interface:
                component["data_bridge"] = first_interface["bridge"]
        if "interfaces" in vm_info and len(vm_info["interfaces"]) > 1:
            second_interface = vm_info["interfaces"][1]
            if "bridge" in second_interface:
                component["access_bridge"] = second_interface["bridge"]

        self._setup_nsgv_component(component)

    def _run_on_hypervisor(self, username, hostname, command):
        return self._run_shell("ssh -oPasswordAuthentication=no  "
                               "-oLogLevel=ERROR -oStrictHostKeyChecking=no "
                               "%s@%s %s " % (username, hostname, command))

    def _import_csv(self):
        deployment_dir = self._get_deployment_dir()
        if deployment_dir is None:
            return

        try:
            from convert_csv_to_deployment import CsvDeploymentConverter
            converter = CsvDeploymentConverter()
        except ImportError:
            self._print(
                "Could not import the libraries to parse CSV files."
                "  Please make sure setup.sh has been run.")
            return

        valid = False
        while not valid:
            csv_file = self._input("Please enter the path to the CSV file", "")

            if csv_file == "" or not os.path.isfile(csv_file):
                choice = self._input(
                    "File not found.  Would you like to skip the import?",
                    0, ["(Y)es", "(n)o"])
                if choice != 1:
                    self._print("Skipping import step...")
                    return
            else:
                valid = True

        try:
            converter.convert(csv_file, deployment_dir)
        except Exception as e:
            self._print(
                "The following errors occurred while parsing the CSV file")
            self._print(str(e))
            self._print("Please correct these and rerun this step")
            return

        data = converter.get_data()
        self.state["csv_data"] = data
        self._print("Imported the following schemas from CSV: " +
                    ", ".join(data.keys()))

        self._read_csv_data(data)

    def _read_csv_data(self, data):

        for schema_name in data:
            if type(data[schema_name]) == list:
                for component in data[schema_name]:
                    if "target_server" in component:
                        self._append_target_server(component["target_server"])

        if "common" in data:
            if "mgmt_bridge" in data["common"]:
                self.state["mgmt_bridge"] = data["common"]["mgmt_bridge"]
            if "data_bridge" in data["common"]:
                self.state["data_bridge"] = data["common"]["data_bridge"]
            if "access_bridge" in data["common"]:
                self.state["access_bridge"] = data["common"]["access_bridge"]

    def _check_skip_for_csv(self, schema_name):
        if "csv_data" in self.state and schema_name in self.state["csv_data"]:
            self._print("This step has been handled via import from CSV.")

            choice = self._input("Do you still wish to continue?",
                                 1, ["(y)es", "(N)o"])
            if choice == 1:
                self._print("Skipping step...")
                return True

        return False

    def _setup_dns(self, deployment, data):
        self._print(self._get_field(data, "dns_setup_msg"))

        dns_domain_default = None
        if "dns_domain" in deployment:
            dns_domain_default = deployment["dns_domain"]

        dns_domain = self._input("Top level DNS domain?", dns_domain_default,
                                 datatype="hostname")
        deployment["dns_domain"] = dns_domain
        self.state["dns_domain"] = dns_domain

        if "vsd_fqdn_global" in deployment:
            vsd_fqdn_default = deployment["vsd_fqdn_global"]
        else:
            vsd_fqdn_default = "xmpp"

        self._print(self._get_field(data, "vsd_fqdn_msg"))

        vsd_fqdn = self._input("VSD FQDN (we'll add .%s)" % dns_domain,
                               vsd_fqdn_default, datatype="hostname")

        if not vsd_fqdn.endswith(dns_domain):
            vsd_fqdn += "." + dns_domain

        deployment["vsd_fqdn_global"] = vsd_fqdn

        if "dns_server_list" in deployment:
            dns_servers_default = ", ".join(deployment["dns_server_list"])
        else:
            dns_servers_default = None

        dns_server_list = None

        while dns_server_list is None:

            dns_server_list = self._input(
                "Enter DNS server IPs in dotted decmial format (separate "
                "multiple using commas)", dns_servers_default)

            dns_server_list = self._format_ip_list(dns_server_list)
            dns_server_list = self._validate_ip_list(dns_server_list)

        deployment["dns_server_list"] = dns_server_list

    def _setup_ntp(self, deployment, data):
        self._print(self._get_field(data, "ntp_setup_msg"))

        if "ntp_server_list" in deployment:
            ntp_servers_default = ", ".join(deployment["ntp_server_list"])
        else:
            ntp_servers_default = None

        ntp_server_list = None
        while ntp_server_list is None:

            ntp_server_list = self._input(
                "Enter NTP server IPs in dotted decmial format (separate "
                "multiple using commas)", ntp_servers_default)

            ntp_server_list = self._format_ip_list(ntp_server_list)
            ntp_server_list = self._validate_ip_list(ntp_server_list)

        deployment["ntp_server_list"] = ntp_server_list

    def _format_ip_list(self, ip_str):
        return [x.strip() for x in ip_str.split(",")]

    def _validate_ip_list(self, ip_list):
        for ip in ip_list:
            if self._validate_ipaddr(ip) is None:
                self._print("\n%s is not a valid IP address\n" % ip)
                return None

        return ip_list

    def _validate_hostname_list(self, hostname_list):
        for hostname in hostname_list:
            if self._validate_hostname(hostname) is None:
                self._print("\n%s is not a valid hostname\n" % hostname)
                return None

        return hostname_list

    def _setup_unzip_dir(self, deployment):
        if "nuage_unzipped_files_dir" in self.state:
            unzip_default = self.state["nuage_unzipped_files_dir"]
        elif ("nuage_unzipped_files_dir" in deployment and
              deployment["nuage_unzipped_files_dir"] != ""):
            unzip_default = deployment["nuage_unzipped_files_dir"]
        else:
            unzip_default = None

        unzip_dir = self._input(
            "Please enter the directory containing unzipped images",
            unzip_default)

        self.state["nuage_unzipped_files_dir"] = unzip_dir
        deployment["nuage_unzipped_files_dir"] = unzip_dir

    def _setup_bridges(self, deployment, data):
        self._print(self._get_field(data, "bridge_setup_msg"))

        if "mgmt_bridge" in deployment:
            mgmt_bridge_default = deployment["mgmt_bridge"]
        else:
            mgmt_bridge_default = ""

        mgmt_bridge = self._input("Management bridge name",
                                  mgmt_bridge_default)

        deployment["mgmt_bridge"] = mgmt_bridge
        if mgmt_bridge != "":
            self.state["mgmt_bridge"] = mgmt_bridge

        if "data_bridge" in deployment:
            data_bridge_default = deployment["data_bridge"]
        else:
            data_bridge_default = ""

        data_bridge = self._input("Data bridge name",
                                  data_bridge_default)

        deployment["data_bridge"] = data_bridge
        if data_bridge != "":
            self.state["data_bridge"] = data_bridge

        if "access_bridge" in deployment:
            access_bridge_default = deployment["access_bridge"]
        else:
            access_bridge_default = ""

        access_bridge = self._input("Access bridge name",
                                    access_bridge_default)

        if access_bridge != "":
            deployment["access_bridge"] = access_bridge
            self.state["access_bridge"] = access_bridge

    def _setup_target_server_type(self):
        if "target_server_type" in self.state:
            return

        self._print("\nPlease choose a target server (hypervisor) type for "
                    "your deployment.\n")

        server_type = self._input("Target server type", 0,
                                  TARGET_SERVER_TYPE_LABELS)

        self.state["target_server_type"] = TARGET_SERVER_TYPE_VALUES[
            server_type]

    def _setup_vcenter(self, deployment):

        default = self._get_value(deployment, "vcenter_datacenter")
        datacenter = self._input("vCenter datacenter for components?", default)
        deployment["vcenter_datacenter"] = datacenter

        default = self._get_value(deployment, "vcenter_cluster")
        cluster = self._input("vCenter cluster for components", default)
        deployment["vcenter_cluster"] = cluster

        default = self._get_value(deployment, "vcenter_datastore")
        datastore = self._input("vCenter datastore for components", default)
        deployment["vcenter_datastore"] = datastore

    def _generate_deployment_file(self, schema, output_file, deployment):
        # Import here because setup may not have been run at the start
        # up of the wizard and the library may not be present
        try:
            import jinja2
            from generate_example_from_schema import ExampleFileGenerator
        except ImportError:
            self._record_problem(
                "deployment_create", "Could not create a deployment file")
            self._print(
                "Cannot write deployment files because libraries are missing."
                "  Please make sure setup.sh has been run.")
            return
        if type(deployment) == list:
            deployment = {schema: deployment}
        deployment["generator_script"] = "Wizard"
        if "target_server_type" in self.state:
            deployment["show_target_server_type"] = (
                self.state["target_server_type"])
        gen_example = ExampleFileGenerator(False, True)
        example_lines = gen_example.generate_example_from_schema(
            os.path.join("schemas", schema + ".json"))
        template = jinja2.Template(example_lines)
        rendered = template.render(**deployment)
        with open(output_file, 'w') as file:
            file.write(rendered.encode("utf-8"))

        self._unrecord_problem("deployment_create")
        self._print("\nWrote deployment file: " + output_file)

    def _setup_upgrade(self, deployment, data):
        self._print(self._get_field(data, "upgrade_msg"))

        if "upgrade_from_version" in deployment:
            upgrade_from_version_default = deployment["upgrade_from_version"]
        else:
            upgrade_from_version_default = None

        upgrade_from_version = self._input("Current running version?",
                                           upgrade_from_version_default,
                                           datatype="version")

        deployment["upgrade_from_version"] = upgrade_from_version

        if "upgrade_to_version" in deployment:
            upgrade_to_version_default = deployment["upgrade_to_version"]
        else:
            upgrade_to_version_default = None

        upgrade_to_version = self._input("Upgrade to version?",
                                         upgrade_to_version_default,
                                         datatype="version")

        deployment["upgrade_to_version"] = upgrade_to_version

    def _get_number_components(self, deployment, data):
        ha_amount = self._get_field(data, "ha_amount")
        deploy_amount = len(deployment)

        if ha_amount == "any":
            item_name = self._get_field(data, "item_name")
            amount = self._input("Number of %ss to setup" % item_name,
                                 deploy_amount,
                                 datatype="int")

            return amount
        else:
            default = 0
            if deploy_amount == 1:
                default = 1

            choice = self._input("Deployment type", default, [
                "(h)igh-availability cluster",
                "(s)tand-alone",
                "(n)one"])

            if choice == 0:
                return ha_amount
            elif choice == 1:
                return 1
            else:
                return 0

    def _setup_hostname(self, deployment, i, item_name):

        dns_domain = None
        dns_message = ""
        if "dns_domain" in self.state:
            dns_domain = self.state["dns_domain"]
            dns_message = " (we'll add .%s)" % dns_domain

        default = None
        component = deployment[i]
        if "hostname" in component:
            default = component["hostname"]
        else:
            default = item_name.lower() + str(i + 1)

        hostname = self._input("Hostname%s" % dns_message, default,
                               datatype="hostname")

        if dns_domain is not None and not hostname.endswith(dns_domain):
            hostname += "." + dns_domain

        component["hostname"] = hostname
        return hostname

    def _setup_ip_addresses(self, deployment, i, hostname, is_vsc):
        component = deployment[i]

        mgmt_ip = self._setup_mgmt_address(component, hostname)
        self._setup_mgmt_prefix(component)
        self._setup_mgmt_gateway(component, mgmt_ip)
        if is_vsc:

            default = self._get_value(component, "ctrl_ip")
            ctrl_ip = self._input("Control IP address for data", default,
                                  datatype="ipaddr")
            component["ctrl_ip"] = ctrl_ip

            default = "24"
            if "ctrl_ip_prefix" in component:
                default = str(component["ctrl_ip_prefix"])

            ctrl_ip_prefix = self._input("Control IP address prefix length",
                                         default, datatype="int")
            component["ctrl_ip_prefix"] = ctrl_ip_prefix

            default = self._get_value(component, "system_ip")
            system_ip = self._input("System IP address for routing", default,
                                    datatype="ipaddr")
            component["system_ip"] = system_ip

        self._setup_target_server(component)

    def _setup_mgmt_address(self, component, hostname):

        default = self._resolve_hostname(hostname)
        if (default is None and "mgmt_ip" in component and
                component["mgmt_ip"] != ""):
            default = component["mgmt_ip"]

        mgmt_ip = self._input("Management IP address", default,
                              datatype="ipaddr")
        component["mgmt_ip"] = mgmt_ip
        return mgmt_ip

    def _setup_mgmt_prefix(self, component):

        default = "24"
        if "mgmt_ip_prefix" in component:
            default = str(component["mgmt_ip_prefix"])

        mgmt_ip_prefix = self._input("Management IP address prefix length",
                                     default, datatype="int")
        component["mgmt_ip_prefix"] = mgmt_ip_prefix
        return mgmt_ip_prefix

    def _setup_mgmt_gateway(self, component, mgmt_ip):

        if "mgmt_gateway" in self.state:
            default = self.state["mgmt_gateway"]
        elif "mgmt_gateway" in component and component["mgmt_gateway"] != "":
            default = component["mgmt_gateway"]
        else:
            octets = mgmt_ip.split(".")
            octets.pop()
            octets.append("1")
            default = ".".join(octets)

        mgmt_gateway = self._input("Management IP gateway", default,
                                   datatype="ipaddr")
        component["mgmt_gateway"] = mgmt_gateway
        self.state["mgmt_gateway"] = mgmt_gateway
        return mgmt_gateway

    def _setup_target_server(self, component):

        if "target_server" in self.state:
            default = self.state["target_server"]
        elif "target_server" in component and component["target_server"] != "":
            default = component["target_server"]
        else:
            default = None

        target_server = self._input("Target server (hypervisor) IP", default,
                                    datatype="hostname")
        component["target_server"] = target_server
        self.state["target_server"] = target_server

        self._append_target_server(target_server)

        return target_server

    def _append_target_server(self, target_server):
        if "all_target_servers" not in self.state:
            self.state["all_target_servers"] = list()

        if target_server not in self.state["all_target_servers"]:
            self.state["all_target_servers"].append(target_server)

    def _resolve_hostname(self, hostname):
        try:
            rc, output_lines = self._run_shell(
                "getent hosts %s" % hostname)
            if rc == 0:
                self._unrecord_problem("dns_resolve")
                self._print("")
                return output_lines[0].split(" ")[0]
            else:
                self._record_problem(
                    "dns_resolve", "Could not resolve hostnames with DNS")

                self._print(
                    u"\nCould not resolve %s to an IP address, this is "
                    u"required for MetroAE to operate.  Is the hostname "
                    u"defined in DNS?" % hostname)
        except Exception as e:
            self._record_problem(
                "dns_resolve", "Error while resolving hostnames with DNS")
            self._print("\nAn error occurred while resolving hostname: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return None

    def _setup_vmname(self, deployment, i, hostname, with_upgrade):
        component = deployment[i]

        dns_domain = None
        if "dns_domain" in self.state:
            dns_domain = self.state["dns_domain"]

        if "vmname" in component:
            default = component["vmname"]
        elif dns_domain is not None and hostname.endswith(dns_domain):
            default = hostname[0:-len(dns_domain) - 1]
        else:
            default = hostname

        vmname = self._input("VM name", default)
        component["vmname"] = vmname

        if with_upgrade:
            default = "new-" + vmname
            upgrade_vmname = self._input("Upgrade VM name", default)
            component["upgrade_vmname"] = upgrade_vmname

    def _setup_vnsutils(self, component, i):

        dns_domain = None
        dns_message = ""
        if "dns_domain" in self.state:
            dns_domain = self.state["dns_domain"]
            dns_message = " (we'll add .%s)" % dns_domain

        default = None
        if "data_fqdn" in component and component["data_fqdn"] != "":
            default = component["data_fqdn"]
        else:
            default = "vnsutil%d.data" % (i + 1)

        hostname = self._input("Data network FQDN%s" % dns_message, default,
                               datatype="hostname")

        if dns_domain is not None and not hostname.endswith(dns_domain):
            hostname += "." + dns_domain

        component["data_fqdn"] = hostname

        default = self._resolve_hostname(hostname)
        if (default is None and "data_ip" in component and
                component["data_ip"] != ""):
            default = component["data_ip"]

        data_ip = self._input("Data network IP address", default,
                              datatype="ipaddr")
        component["data_ip"] = data_ip

        default = self._get_value(component, "data_netmask")
        if default is None:
            default = "255.255.255.0"
        address = self._input("Data network subnet mask", default,
                              datatype="ipaddr")
        component["data_netmask"] = address

        choice = self._input("Will you use DHCP on the VNSUtil?", 0,
                             ["(Y)es", "(n)o"])

        if choice == 1:
            if "data_subnet" in component:
                del component["data_subnet"]
            if "nsgv_gateway" in component:
                del component["nsgv_gateway"]
            return

        default = self._get_value(component, "data_subnet")
        if default is None:
            octets = data_ip.split(".")
            octets.pop()
            octets.append("0")
            default = ".".join(octets)

        data_subnet = self._input("Data IP subnet for DHCP",
                                  default, datatype="ipaddr")
        component["data_subnet"] = data_subnet
        self.state["data_subnet"] = data_subnet

        default = self._get_value(component, "nsgv_gateway")
        if default is None:
            octets = data_ip.split(".")
            octets.pop()
            octets.append("1")
            default = ".".join(octets)

        nsgv_gateway = self._input("Data IP gateway given by DHCP",
                                   default, datatype="ipaddr")
        component["nsgv_gateway"] = nsgv_gateway
        self.state["nsgv_gateway"] = nsgv_gateway

    def _setup_nsgv_component(self, component):

        default = 1
        if "bootstrap_method" in component:
            if component["bootstrap_method"] == "none":
                default = 0
            elif component["bootstrap_method"] == "zfb_metro":
                default = 1
            elif component["bootstrap_method"] == "zfb_external":
                default = 2
            elif component["bootstrap_method"] == "activation_link":
                default = 3

        choice = self._input("Bootstrap method", default, [
            "(n)one       - Do not bootstrap",
            "(M)etro      - MetroAE will perform the bootstrap",
            "(e)xternal   - Use an external ISO file to bootstrap",
            "(a)ctivation - Use an activation link for bootstrap"])

        if choice == 0:
            component["bootstrap_method"] = "none"
        elif choice == 1:
            component["bootstrap_method"] = "zfb_metro"
            self.state["metro_bootstrap"] = True
            self._bootstrap_component_metro(component)
        elif choice == 2:
            component["bootstrap_method"] = "zfb_external"
            self._bootstrap_component_external(component)
        elif choice == 3:
            component["bootstrap_method"] = "activation_link"

    def _bootstrap_component_metro(self, component):
        default = self._get_value(component, "nsg_name")
        if default is None:
            default = self._get_value(component, "vmname")
        name = self._input("NSGv name on VSD", default)
        component["nsg_name"] = name

        default = self._get_value(component, "nsgv_ip")
        address = self._input("IP address for NSGv", default,
                              datatype="ipaddr")
        component["nsgv_ip"] = address
        component["match_type"] = "ip_address"
        component["match_value"] = address
        default = self._get_value(component, "nsgv_mac")
        mac = self._input("MAC address for NSGv", default)
        component["nsgv_mac"] = mac

        default = self._get_value(component, "network_port_name")
        network_port = self._input("Name for network port", default)
        component["network_port_name"] = network_port

        default = self._get_value(component, "access_port_name")
        access_port = self._input("Name for access port", default)
        component["access_port_name"] = access_port

        default = self._get_value(component, "access_port_vlan_range")
        vlan_range = self._input("VLAN range for access port "
                                 "(format: <start>-<end>)", default)
        component["access_port_vlan_range"] = vlan_range

        default = self._get_value(component, "access_port_vlan_number")
        vlan = self._input("Vlan number for access port", default,
                           datatype="int")
        component["access_port_vlan_number"] = vlan

    def _bootstrap_component_external(self, component):
        default = None
        default_path = component.get("iso_path")
        default_file = component.get("iso_file")
        if default_path is not None and default_file is not None:
            default = os.path.join(default_path, default_file)

        path_file = ""
        while "/" not in path_file:
            path_file = self._input("Full path to ISO file", default)
        path, file = os.path.split(path_file)
        component["iso_path"] = path
        component["iso_file"] = file

    def _setup_bootstrap(self, deployment, data):

        default = self._get_value(deployment, "nsgv_organization")
        org = self._input("Enterprise for NSGvs", default)
        deployment["nsgv_organization"] = org

        default = self._get_value(deployment, "proxy_user_first_name")
        first_name = self._input("First name for proxy user", default)
        deployment["proxy_user_first_name"] = first_name

        default = self._get_value(deployment, "proxy_user_last_name")
        last_name = self._input("Last name for proxy user", default)
        deployment["proxy_user_last_name"] = last_name

        default = self._get_value(deployment, "proxy_user_email")
        email = self._input("Email address for proxy user", default)
        deployment["proxy_user_email"] = email

        default = self._get_value(deployment, "nsg_infra_profile_name")
        profile_name = self._input("Name of NSG infrastructure profile",
                                   default)
        deployment["nsg_infra_profile_name"] = profile_name

        default = self._get_value(deployment, "nsg_template_name")
        template_name = self._input("Name of NSG template", default)
        deployment["nsg_template_name"] = template_name

        default = self._get_value(deployment, "proxy_dns_name")
        dns_name = self._input("DNS name of proxy (on data network)", default)
        deployment["proxy_dns_name"] = dns_name

        default = self._get_value(deployment, "vsc_infra_profile_name")
        profile_name = self._input("Name of VSC infrastructure profile",
                                   default)
        deployment["vsc_infra_profile_name"] = profile_name

        default = self._get_value(deployment, "first_controller_address")
        address = self._input("IP address of primary VSC controller"
                              " (on data network)", default,
                              datatype="ipaddr")
        deployment["first_controller_address"] = address

        choice = self._input("Do you have a secondary VSC controller?", 0,
                             ["(Y)es", "(n)o"])

        if choice == 1:
            if "second_controller_address" in deployment:
                del deployment["second_controller_address"]
            return

        default = self._get_value(deployment, "second_controller_address")
        address = self._input("IP address of secondary VSC controller"
                              " (on data network)",
                              default, datatype="ipaddr")
        deployment["second_controller_address"] = address

    def _setup_ssh(self, username, hostname):
        self._print("Adding SSH keys for %s@%s, may ask for password" % (
            username, hostname))
        try:
            options = ""
            if self.in_container:
                options = "-i /source/id_rsa.pub -o StrictHostKeyChecking=no "
            else:
                self._setup_ssh_key()
            rc, output_lines = self._run_shell(
                "ssh-copy-id %s%s@%s" % (options, username, hostname))
            if rc == 0:
                self._unrecord_problem("ssh_keys")
                self._print("\nSuccessfully setup SSH on host %s" % hostname)
                return True
            else:
                self._record_problem(
                    "ssh_keys", "Could not setup password-less SSH")
                self._print("\n".join(output_lines))
                self._print(
                    u"\nCould not add SSH keys for %s@%s, this is required"
                    u" for MetroAE to operate." % (username, hostname))
        except Exception as e:
            self._record_problem(
                "ssh_keys", "Error while setting up password-less SSH")
            self._print("\nAn error occurred while setting up SSH: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return False

    def _setup_ssh_key(self):
        rc, output_lines = self._run_shell("stat ~/.ssh/id_rsa.pub")
        if rc != 0:
            self._print("\nCould not find your SSH public key "
                        "~/.ssh/id_rsa.pub\n")

            choice = self._input("Do you wish to generate a new SSH keypair?",
                                 0, ["(Y)es", "(n)o"])

            if choice == 0:
                rc, output_lines = self._run_shell('ssh-keygen -P "" '
                                                   '-f ~/.ssh/id_rsa')

                if rc == 0:
                    self._print("\nSuccessfully generated an SSH keypair")
                    return True
                else:
                    self._record_problem(
                        "ssh_keys", "Could not generate SSH keypair")
                    self._print("\n".join(output_lines))
                    self._print(
                        "\nCould not generate an SSH keypair, this is "
                        "required for MetroAE to operate.")
                    return False

        return True

    def _verify_ssh(self, username, hostname):
        try:
            rc, output_lines = self._run_shell(
                "ssh -oPasswordAuthentication=no %s@%s exit 0" % (
                    username, hostname))
            if rc == 0:
                self._unrecord_problem("ssh_access")
                self._print("\nSuccessfully connected via SSH to host %s" %
                            hostname)
                return True
            else:
                self._record_problem(
                    "ssh_access", "Could not connect via password-less SSH")
                self._print("\n".join(output_lines))
                self._print(
                    u"\nCould not connect via SSH to %s@%s, this is required"
                    u" for MetroAE to operate." % (username, hostname))
        except Exception as e:
            self._record_problem(
                "ssh_access", "Error while connecting to host via SSH")
            self._print("\nAn error occurred while connecting to host via "
                        " SSH: " + str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return False

    def _verify_bridge(self, username, hostname, bridge):
        try:
            rc, output_lines = self._run_shell(
                "ssh -oPasswordAuthentication=no %s@%s PATH=$PATH ip addr show"
                " dev %s" % (
                    username, hostname, bridge))
            if rc == 0:
                self._unrecord_problem("bridge")
                self._print("\nSuccessfully verified bridge %s on host %s" % (
                            bridge, hostname))
                return True
            else:
                self._record_problem(
                    "bridge", "Bridge not present on target server host")
                self._print("\n".join(output_lines))
                self._print(
                    u"\nBridge %s not present on %s, this is required"
                    u" for components to communicate." % (bridge, hostname))
        except Exception as e:
            self._record_problem(
                "bridge", "Error while verifying bridge interfaces")
            self._print("\nAn error occurred while verifying bridge interface "
                        " via SSH: " + str(e))
            self._print("Please contact: " + METROAE_CONTACT)

        return False


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
