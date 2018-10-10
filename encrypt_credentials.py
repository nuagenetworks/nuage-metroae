import argparse
import sys
import yaml
import json
from ansible.parsing.vault import VaultEditor, VaultSecret

class VaultYaml(unicode): 
    pass


def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar("!vault", data, style='|')


def encrypt_credentials_file(passcode):
    yaml.add_representer(VaultYaml, literal_unicode_representer)
    #todo: what happens for non-default
    credentials_file = 'deployments/default/credentials.yml'
    with open(credentials_file, 'r') as file:
        credentials = yaml.safe_load(file.read())

    with open('schemas/credentials.json') as credentials_schema:    
        data = yaml.safe_load(json.dumps(json.load(credentials_schema)))
    props = data['properties']
    encryt_credentials_list = []
    for k,v in props.items():
        if ('encrypt' not in v) or v['encrypt']:
            encryt_credentials_list.append(k)

    if credentials is not None:
        for cred in encryt_credentials_list:
            if cred in credentials:
                secret = VaultSecret(passcode)
                editor = VaultEditor()
                vaultCode = editor.encrypt_bytes(credentials[cred], secret)
                credentials[cred] = VaultYaml(vaultCode)
        with open(credentials_file, 'w') as file:
            yaml.dump(credentials, file, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt user credentials file')
    parser.add_argument("--passcode", help="Passcode to vault encrypt credentials file")
    args = parser.parse_args()

    if not args.passcode:
        print "Missing passcode for encryption"
        parser.print_help()
        sys.exit()

    encrypt_credentials_file(args.passcode)


if __name__ == '__main__':
    main()
