#!/usr/bin/env python
import sys
import yaml
import getpass
import argparse
import jinja2
import os
from ansible.parsing.vault import VaultEditor, VaultSecret, is_encrypted
from generate_example_from_schema import ExampleFileGenerator

DEPLOYMENT_DIR = 'deployments'


class VaultYaml(unicode):
    pass


def vault_constructor(loader, node):
    return node.value


def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar("!vault", data, style='|')


def encrypt_credentials_file(passcode, deployment_name):
    yaml.add_constructor(u'!vault', vault_constructor)
    if os.path.isfile(deployment_name):
        credentials_file = deployment_name
    elif os.path.isdir(deployment_name):
        credentials_file = os.path.join(
            deployment_name, 'credentials.yml')
    else:
        credentials_file = os.path.join(
            DEPLOYMENT_DIR, deployment_name, 'credentials.yml')
    with open(credentials_file, 'r') as file:
        credentials = yaml.load(file.read().decode("utf-8"),
                                Loader=yaml.Loader)

    with open('schemas/credentials.json') as credentials_schema:
        data = yaml.load(credentials_schema.read().decode("utf-8"),
                         Loader=yaml.Loader)
    props = data['items']['properties']
    do_not_encrypt_list = []
    for k, v in props.items():
        if ('encrypt' in v) and (not v['encrypt']):
            do_not_encrypt_list.append(k)

    if credentials is not None:
        for cred_set in credentials:
            for cred in cred_set.keys():
                if cred not in do_not_encrypt_list:
                    secret = VaultSecret(passcode)
                    editor = VaultEditor()
                    if not is_encrypted(cred_set[cred]):
                        vaultCode = editor.encrypt_bytes(cred_set[cred],
                                                         secret)
                    else:
                        vaultCode = cred_set[cred]
                    cred_set[cred] = '!vault |\n' + (vaultCode)

        gen_example = ExampleFileGenerator(False, True)
        example_lines = gen_example.generate_example_from_schema(
            'schemas/credentials.json')
        template = jinja2.Template(example_lines)
        credentials = template.render(credentials=credentials)
        with open(credentials_file, 'w') as file:
            file.write(credentials.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt user credentials file')
    parser.add_argument(
        "deployment",
        nargs='?',
        help="Optional deployment name - will default to 'default' deployment",
        default="default")
    args = parser.parse_args()

    if "METROAE_PASSWORD" in os.environ:
        passcode = os.environ["METROAE_PASSWORD"]
    else:
        try:
            print "This file will encrypt user credentials for MetroAE"
            print ("All user comments and unsupported fields in the "
                   "credentials file will be lost")
            print "Press Ctrl-C to cancel"
            while True:
                passcode = getpass.getpass()
                confirm_passcode = getpass.getpass("Confirm passcode:")
                if passcode != confirm_passcode:
                    print "Passcodes do not match. Please reenter"
                else:
                    break
        except Exception:
            print "Error in getting passcode from command line"
            sys.exit()

    encrypt_credentials_file(passcode, args.deployment)


if __name__ == '__main__':
    main()
