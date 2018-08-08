# Vault encrypt your user data files 

This Document provides a way to encrypt your user data files in MetroAE using Ansible Vault encryption. 
Vault encrypted files safeguard user sensitive information from being decoded.

## Steps for encrypting user data files

### 1. Create a vault encrytion passcode file

User can create a file with a master passcode in it. This passcode can be used to encode/decode all other user data files. 
In general it is a good idea to keep this file outside of the source code.

### 2. Encrypt sensitive user data file using the above passcode file

ansible-vault encrypt user_creds.yml --vault-password-file myvault.txt

### 3. While running Metro commands, supply the vault password file as option

./metro-ansible myplaybook --vault-password-file myvault.txt

