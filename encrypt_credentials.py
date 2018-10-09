import argparse
import sys
import yaml
from ansible.parsing.vault import VaultAES256
from ansible.parsing.vault import VaultSecret

def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

def encrypt_credentials_file(passcode):
    #todo: what happens for non-default
    credentials_file = 'deployments/default/credentials.yml'
    with open(credentials_file, 'r') as file:
        credentials = yaml.safe_load(file.read())

    print credentials
    if credentials is not None:
        # Get the credentials list from schema
        encryt_credentials_list = ['vcenter_password', 'vsd_auth_password']

        for cred in encryt_credentials_list:
            if cred in credentials:
                # encrypt passcode with password
                secret = VaultSecret(passcode)
                vault = VaultAES256.encrypt(credentials[cred], secret)
                b_HEADER = b'$ANSIBLE_VAULT'
                b_version = u'1.1'
                b_cipher_name = u'AES256'
                header_parts = [ b_HEADER, b_version, b_cipher_name]
                header = b';'.join(header_parts)
                b_vaulttext = [header]
                b_vaulttext += [vault[i:i + 80] for i in range(0, len(vault), 80)]
                b_vaulttext += [b'']
                b_vaulttext = b'\n'.join(b_vaulttext)
                
                credentials[cred] = str(b_vaulttext)
                #result = VaultAES256.decrypt(vault, secret)
                #print result
        print credentials
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
