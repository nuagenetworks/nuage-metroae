# Encrypting Sensitive Data in MetroAE

You can safeguard sensitive data in MetroAE by encrypting files with MetroAE's encryption tool. Your credentials can be encrypted when provided through your `credentials.yml` deployment file or in a `credentials` sheet in your Excel deployment spreadsheet. The steps for both are below. We use Ansible's vault encoding in the background. More details about the vault feature can be found in [documentation](https://docs.ansible.com/ansible/2.4/vault.html) provided by Ansible.

The steps for encrypting your `credentials.yml` deployment file are as follows:

### 1. Create the credentials file to be encrypted

In your MetroAE deployment folder, create or edit the `credentials.yml` to store credentials required for various Nuage components. This file will be encrypted.

### 2. Encrypt `credentials.yml`

To encrypt `credentials.yml`, run the following command:  
```
metroae tools encrypt credentials [deployment_name]
```

The default deployment name is `default` if not specified. This command will prompt for master passcode to encrypt the file and will also prompt for confirming passcode.
Note: All user comments and unsupported fields in the credentials file will be lost.

To encrypt your credentials in an Excel spreadsheet, the steps are:

### 1. Create your Excel deployment

We provide examples of Excel spreadsheets in `examples/excel/`. You can use these as guides to create your deployment. Once you fill out the `credentials` sheet in your spreadsheet, you can proceed to the next step which will encrypt the `credentials` sheet (the rest of your deployment will be unchanged).

### 2. Encrypt `credentials` sheet

To encrypt your `credentials` sheet, run the following command:
```
metroae tools encrypt credentials excel <path_to_excel_spreadsheet>
```
There is no default spreadsheet - if you don't specify a path the command will fail. The encryption behavior is the same as if you were to encrypt a `credentials.yml` deployment file. You will be prompted for, and asked to confirm, a master password to encrypt the file. All user comments and unsupported fields in the credentials file will be lost.

You can then proceed to run MetroAE using your Excel spreadsheet/

### Running MetroAE with encrypted credentials

While running MetroAE commands you can supply the MetroAE passcode via prompt or by setting an environment variable
```
metroae <workflow> <component> [action] [deployment_name]
```

This command prompts you to enter the master passcode that you used to encrypt the credentials file.
Alternatively, if you have the environment variable METROAE_PASSWORD set to the right passcode, MetroAE does not prompt for the passcode.

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
