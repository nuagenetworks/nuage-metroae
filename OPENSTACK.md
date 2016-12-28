# Support for deploying VSP components in OpenStack through metro(limited support)
# Note: This is purely for internal lab. Not meant for customer use.

Using metro, users can deploy VSP components into OpenStack. Apart from the VSP components there is also support for deploying OpenStack Controller (OSC) using packstack and adding computes(vms) to the OSC by replacing OVS packages with nuage VRS. Users can also make backups of an entire project or set of VMs in a project using snapshot role. 

These snapshots are stored downloaded to local machine. Currently they are not archived or exported to a remote machine. So, make sure the local machine has enough storage.

An infra VM is aslo deployed which acts as private DNS server and ntp server for VSD and VSC. The DNS entries are automatically populated with the delp of vsd-deploy and vsc-deploy roles. For this reason the user has to specify the infra VM FQDN for VSD and VSC build-vars

To summarize, these are the following components/roles supported by metro on OpenStack

```
Deploy INFRA server
Deploy VSD (Standalone)
Deploy a single VSC
Deploy OpenStack controller (OSC)
Deploy OpenStack computes(VMs)
Add computes to OSC and add VRS packages
Support for project/vms snapshot
```

The build playbook (`build.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-playbook build.yml` will use the variables defined in `build-vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build.yml` playbook will do all the work for you.

Note that the syntax of the contents of `build-vars.yml` must be precise. If things get messed up, we have provided the `reset_build.yml` playbook to let you start over. *When you run `./metro-ansible rest_build.yml`, the contents of `build-vars.yml` will be overwritten, the `hosts` file will be destroyed, the `host_vars` directory will be destroyed, and the `group_vars` directory will be destroyed. The variable configuration of metro will be reset to factory settings! You may lose your work!* A backup copy of `build-vars.yml` will be created with a proper timestamp in case you did not mean it.

To run the build, execute:

`ansible-playbook build.yml`

or

`./metro-ansible build.yml`

To reset the build to factory settings, execute:

`ansible-playbook reset_build.xml`

or

`./metro-ansible rest_build.yml`

# nuage_unpack playbook

When the `build.yml` playbook is executed, it will first check the setting for the parameter `nuage_unpacked` in the vars section of the plabook. When `nuage_unpacked` is set to `false`, the `nuage-unpack` role will be executed prior to setting other parameters. The `nuage_unpack` role is useful when you download the Nuage Networks software as a set of archives for each component of the solution. To deploy the software using Metro, only a few of the binaries in those archives are required. As such the `nuage-unpack` role will analyze all the archives, extract the necessary binaries, and store them in a configurable directory.

You can also choose to unpack the binaries yourself, skipping the `nuage-unpack` role by setting `nuage_unpacked` to `true` in `build.yml`. In such a case, the playbooks will assume that you have already unpacked the binaries into the appropriate locations, as shown below.

```
<your_path>/vsc
<your_path>/vrs
<your_path>/dockermon
<your_path>/vstat
<your_path>/vns/nsg
<your_path>/vns/nsg/aws
<your_path>/vns/util
<your_path>/nuage_os
```

You can also choose to run the `nuage-unpack` role manually by executing `./metro-ansible nuage_unpack.yml`
The `nuage-unpack` role also uses Ansible tags to limit the extraction or variable setting to a particular component of choice.
# Reference

For reference, here is a description of the contents of the `build-vars.yml` file, with comments:

```
#    # The directory where the Nuage Networks binariy archives are located. This is only
#    # required if nauge_unpacked == false. See below.
#    nuage_release_src_path: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where to extract the relevant Nuage Networks binaries to
#    nuage_unpacked_dest_path: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Parameter used to define the Hypervisor-Architecture (One of: el6|el7|ubuntu)
#    nuage_target_architecture: "el7"
#    # Parameter to define whether binaries have already been extracted
#    # If true, the playbooks will *not* unpack. Files in nnuage_unpacked_dest_path
#    # will be used as is. If false, the nuage_unpack role will be executed.
#    nuage_unpacked: true
#    # Nuage OpenStack release
#    # required to populate/unpack nuage openstack packages
#    # supported OpenStack release for metro - liberty, mitaka
#    nuage_os_release: "liberty"
#    VSD
#    # When True or undefined, all VSDs will be configured stand-alone. 
#    # Only standlone mode is supported on OpenStack through metro
#    vsd_standalone: True
#    # A dictionary of params for INFRA server
#    myinfras:
#          # The fqdn of this INFRA instance
#      - { hostname: infra.example.com,
#          # The target server type where this INFRA instance will run. Possible values: heat
#          target_server_type: heat,
#          # INFRA image to be used. Must exist on OpenStack
#          infra_image: centos7,
#          # INFRA flavor to be used. Must exist  on OpenStack
#          infra_flavor: m1.medium,
#          # INFRA network. Must exist on OpenStack
#          infra_network: mgmt }
#    # A dictionary of params for 1 VSD
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vsd1.example.com,
#          # The target server type where this VSD instance will run. Possible values: heat
#          target_server_type: heat,
#          # VSD image to be used. Must exist on OpenStack
#          vsd_image: vsd-r4,
#          # VSD flavor to be used. Must exist  on OpenStack
#          vsd_flavor: m1.xlarge,
#          # VSD network. Must exist on OpenStack
#          vsd_network: mgmt,
#          # INFRA server vm fqdn name
#          infra_server_name: infra.example.com }
#
#    VSC
#    # A dictionary of params for 1 VSC
#    myvscs:
#          # The fqdn of this VSC instance
#      - { hostname: vsc1.example.com,
#          # The target server type where this VSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # VSC image to be used. Must exist on OpenStack
#          vsc_image: vsc-r4,
#          # VSC flavor to be used. Must exist  on OpenStack
#          vsc_flavor: vsc-r4,
#          # VSC network. Must exist on OpenStack
#          vsc_management_network: mgmt,
#          # VSC control network. Must exist on OpenStack
#          vsc_control_network: control_net, 
#          # The FQDN of the VSD this VSC should conect to
#          vsd_fqdn: vsd1.example.com,
#          # The system IP address and name for this VSC instance
#          system_ip: 1.1.1.2,
#          # The XMPP user name for login to VSD
#          xmpp_username: vsc,
#          # INFRA server vm fqdn name
#          infra_server_name: infra.example.com }
#
#    # A dictionary of params for 1 OSC
#    myoscs:
#          # The fqdn of this OSC instance
#      - { hostname: osc1.example.com,
#          # The target server type where this OSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # OSC image to be used. Must exist on OpenStack
#          osc_image: cenots7,
#          # OSC flavor to be used. Must exist  on OpenStack
#          osc_flavor: m1.medium,
#          # OSC network. Must exist on OpenStack
#          osc_network: mgmt,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # VSD IP. This is later used in a rest proxy config file to integrate OSC with VSD
#          vsd_ip: 192.168.10.20,
#          # Primary controller IP. This is used to configure VRS on the computes
#          primary_controller: 192.168.10.21 }
#
#    # A dictionary of params for 1 or more OpenStack compute vms
#    myoscomputes:
#          # The fqdn of this OS-COMPUTE instance
#      - { hostname: oscompute1.example.com,
#          # The target server type where this OS-COMPUTE instance will run. Possible values: heat
#          target_server_type: heat,
#          # OS-COMPUTE image to be used. Must exist on OpenStack
#          compute_image: cenots7,
#          # OS-COMPUTE flavor to be used. Must exist  on OpenStack
#          compute_flavor: m1.medium,
#          # OS-COMPUTE network. Must exist on OpenStack
#          compute_network: mgmt,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # OSC Serer name. FQDN of the OpenStack Controller
#          osc_server_name: osc1.example.com }
#    OpenStack credentials for authentication
#    os_auth:
#          # The username for OpenStack project
#          username: admin
#          # Password for OpenStack project
#          password: admin
#          # OpenStack project name
#          project_name: jen
#          # OpenStack keystone url
#          auth_url: 'http://10.0.0.4:5000/v2.0'
#
#    # ENVIRONMENT
#    # The hostname or IP address of the ansible machine
#    ansible_deployment_host: 135.227.181.232
#    # NTP servers the INFRA VM can sync to
#    # One or more ntp servers are required
#    ntp_server_list:
#      - 135.227.181.232
#      - 128.138.141.172
#    # DNS configuration
#    # One or more dns servers are required
#    dns_server_list:
#      - 192.168.122.1
#      - 128.251.10.145
#    # The dns search domain
#    dns_domain: example.com
```
