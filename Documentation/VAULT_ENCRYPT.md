# Encrypting Sensitive Data with Ansible Vault  
You can safeguard sensitive data in Metro&#198; by encrypting files with Ansible's vault feature. See the steps below for instructions on how to encrypt `user_creds.yml`. More details about the vault feature can be found in [documentation](https://docs.ansible.com/ansible/2.4/vault.html) provided by Ansible.  
### 1. Create a vault encryption passcode file  
 Create a file containing a master passcode (example file name: myvault.txt). This passcode can be used to encode and decode all other user data files. It's generally a good idea to keep this file outside of the source code.  
### 2. Encrypt `user_creds.yml`  
  To encrypt `user_creds.yml` with the passcode file that you created in step one above, run the following command:  
  ```
  ansible-vault encrypt user_creds.yml --vault-password-file myvault.txt
  ```     
### 3. Pass the vault password file option  
  While running Metro&#198; commands you can supply the vault password file as an option by running the following command:
```
./metro-ansible the_name_of_the_playbook --vault-password-file myvault.txt
```  
## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.MD) to Nuage Metro&#198; by submitting your own code to the project.
