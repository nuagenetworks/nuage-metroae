# Encrypting Sensitive Data in MetroAE

You can safeguard sensitive data in MetroAE by encrypting files with MetroAE's encryption tool. Your credentials can be encrypted when provided through your `credentials.yml` deployment file or in a `credentials` sheet in your Excel deployment spreadsheet. We use Ansible's vault encoding in the background. More details about the vault feature can be found in [documentation](https://docs.ansible.com/ansible/2.4/vault.html) provided by Ansible.

The steps for encrypting your `credentials.yml` deployment file or your credentials in an Excel spreadsheet are as follows:

### 1a. Create the credentials file to be encrypted

In your MetroAE deployment folder, create or edit the `credentials.yml` to store credentials required for various Nuage components. This file will be encrypted.

### 1b. Create your Excel deployment

We provide examples of Excel spreadsheets in `examples/excel/`. You can use these as guides to create your deployment. Once you fill out the `credentials` sheet in your spreadsheet, you can proceed to the next step which will encrypt the `credentials` sheet (the rest of your deployment will be unchanged).

### 2. Encrypt your credentials

To encrypt your credentials, run the following command:  
```
metroae tools encrypt credentials [deployment_name/path_to_excel_spreadsheet]
```

The default deployment name is `default` if not specified. This command will prompt for master passcode to encrypt the file and will also prompt for confirming passcode.
Note: All user comments and unsupported fields in the credentials file will be lost.

You do not need to provide a deployment name if you're using an Excel spreadsheet.

### 3. Running MetroAE with encrypted credentials

While running MetroAE commands you can supply the MetroAE passcode via prompt or by setting an environment variable
```
metroae <workflow> <component> [action] [deployment_name]
```

This command prompts you to enter the master passcode that you used to encrypt the credentials file.
Alternatively, if you have the environment variable METROAE_PASSWORD set to the right passcode, MetroAE does not prompt for the passcode.

If you are using an Excel spreadsheet, you can convert your Excel spreadsheet into a deployment using the converter script:
```
convert_excel_to_deployment.py [path_to_excel_spreadsheet] [your_deployment_name]
```
or, you can run any `metroae` playbook that invokes the `build` step (all playbooks aside from `nuage_unip` and `reset_build`) to convert your Excel spreadsheet into a deployment. The example below calls `build` directly, but you can use a different playbook:
```
metroae build [path_to_excel_spreadsheet]`
```

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
