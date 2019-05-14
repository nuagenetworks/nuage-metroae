#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import traceback
import yaml

METROAE_CONTACT = "devops@nuagenetworks.net"

WIZARD_SCRIPT = """

- message:
    text: |

      Thank you for using MetroÆ!

      This wizard will walk you through the setup process of MetroÆ
      step-by-step and ensure that all prerequisites are satisfied.

      The following steps will be performed:

- list_steps: {}

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

- step: Create deployment
  message:
    text: Deployment OK!

- message:
    text: |

      The wizard is complete!

"""

STANDARD_FIELDS = ["step", "description"]


class Wizard(object):

    def __init__(self, script=WIZARD_SCRIPT):
        self.progress_display_count = 0
        self.progress_display_rate = 1

        if "NON_INTERACTIVE" in os.environ:
            self.args = list(sys.argv)
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
        self._print(self._get_field(data, "text"))

    def list_steps(self, action, data):
        for step in self.script:
            if "step" in step:
                self._print("  - " + step["step"])

    def verify_install(self, action, data):
        self._print("\nVerifying MetroÆ installation")

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
            return

        missing = self._compare_libraries(required_libraries, output_lines)

        try:
            self.progress_display_rate = 10
            rc, output_lines = self._run_shell("yum list")
            if rc != 0:
                self._print("\n".join(output_lines))
                raise Exception("yum list exit-code: %d" % rc)

            with open("yum_requirements.txt", "r") as f:
                required_libraries = f.read().split("\n")

        except Exception as e:
            self._print("\nAn error occurred while reading pip libraries: " +
                        str(e))
            self._print("Please contact: " + METROAE_CONTACT)
            return

        yum_missing = self._compare_libraries(required_libraries, output_lines)
        missing.extend(yum_missing)

        if len(missing) == 0:
            self._print("\nMetroÆ Installation OK!")
        else:
            self._print("\nYour MetroÆ installation missing libraries:")
            self._print("\n".join(missing))
            self._print(self._get_field(data, "missing_msg"))
            choice = self._input("Do you want to run setup now?", 0,
                                 ["(Y)es", "(n)o"])

            if choice != 1:
                self._print("Running setup (may ask for sudo password)")
                try:
                    rc, output_lines = self._run_shell("sudo ./metro-setup.sh")
                    if rc != 0:
                        self._print("\n".join(output_lines))
                        raise Exception("metro-setup.sh exit-code: %d" % rc)

                    self._print("\nMetroÆ setup completed successfully!")
                except Exception as e:
                    self._print("\nAn error occurred while running setup: " +
                                str(e))
                    self._print("Please contact: " + METROAE_CONTACT)
                    return

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
            value = self._validate_input(self, user_value, default,
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
            self._print("Step: " + action["step"] + "\n")

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
                        missing.append("Requires %s, installed %s" %
                                       (req_lib, inst_lib))
                    break

            if not found:
                missing.append(req_lib)

        return missing


def main():
    try:
        wizard = Wizard()
        wizard()
        # value = wizard._input("Enter VSD mode", 1, ["(S)tand-alone",
        #                                             "(H)igh-availability",
        #                                             "(N)one"])

        # value = wizard._input("Enter IP address", None)
        # print str(value)
    except Exception:
        traceback.print_exc()
        print "\nThere was an unexpected error running the wizard"
        print "Please contact: " + METROAE_CONTACT
        exit(1)


if __name__ == '__main__':
    main()
