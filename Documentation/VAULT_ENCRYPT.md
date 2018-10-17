# Encrypting Sensitive Data in Nuage Metro 
You can safeguard sensitive data in Metro&#198; by encrypting files with Metro&#198;'s encryption tool. See the steps below for instructions on how to encrypt `credentials.yml`. It uses Ansible's vault encoding in the background. More details about the vault feature can be found in [documentation](https://docs.ansible.com/ansible/2.4/vault.html) provided by Ansible.  
### 1. Create the credentials file to be encrypted
  In your Metro deployment folder, create or edit the `credentials.yml` to store credentials required for various Nuage component. This file will be encrypted.  
### 2. Encrypt `credentials.yml`  
  To encrypt `credentials.yml`, run the following command:  
  ```
  python encrypt_credentials.py <deployment_name>
  ```
  Default deployment name is `default` if not specified. This command will prompt for master passcode to encrypt the file and will also prompt for confirming passcode.
  Note: All user comments and unsupported fields in the credentials file will be lost

### 3. Running Metro&#198; with encrypted credentials
  While running Metro&#198; commands you can supply the Metro&#198; passcode via prompt or by setting an environment variable
  ```
  metroae the_name_of_the_playbook
  ```
  This will prompt you to enter the master passcode that you used to encrypt the credentials file. 
  Alternatively, if you have the environment variable METROAE_PASSWORD set to the right passcode, Metro&#198; will not prompt for the passcode.

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
