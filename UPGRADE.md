# Special instructions while upgrade work is in flight...

## Upgrade steps

As of this writing, only `vsc-health` is supported. Other things will be supported shortly. Look here for updates on progress and process.

Using `vsc-health` is a process to use at the moment. You need to:
 
1. Edit build.yml such that the `myvscs` group is populated and the other component sections, e.g. `myvsds`, are removed. I have pasted an example vars section at the bottom of this message. Even though you aren’t deploying anything, you’ll need to make sure nuage_unpacked, nuage_unpacked_dest_path, and nauge_release_src_path are set correctly. Also, you must have the VSC binary files on disk in those locations. In the example I have given you, nuage_unpacked is false, so the playbook will expect to find the VSC gzipped tarball in /home/caso/metro/4.0R4/nuage-packed. (We will soon fix it so that you don’t need to have the archive present…)
1. Edit vsc_health.yml to set the location and file name of the output report. Note that you must change it in two places in that file!
1. Edit roles/vsc-health/vars/main.yml to set test comparison values such as the expected number of BGP peers.
1. Run the build step to populate hosts and variables. ./metro-ansible build.yml is the command.
1. Run the vsc-health check. ./metro-ansible vsc_health.yml
 
## 'build.yml' example

The following is an example of a 'build.yml' file that can be used to prepare for a run of vsc-health against an existing VSP deployment.

```
vars:
    nuage_release_src_path: "/home/caso/metro/4.0R4/nuage-packed"
    nuage_unpacked_dest_path: "/home/caso/metro/4.0R4/nuage-unpacked"
    nuage_unpacked: false
    nuage_target_architecture: "el7"
    vsd_standalone: true
    myvscs:
      - { hostname: jenkinsvsc1.example.com,
          target_server_type: "kvm",
          target_server: 135.227.181.233,
          mgmt_ip: 192.168.122.212,
          mgmt_gateway: 192.168.122.1,
          mgmt_netmask_prefix: 24,
          ctrl_ip: 192.168.100.202,
          ctrl_netmask_prefix: 24,
          vsd_fqdn: jenkinsvsd1.example.com,
          system_ip: 1.1.1.2,
          xmpp_username: jenkinsvsc1,
          vsc_static_route_list: { 0.0.0.0/1 } }
      - { hostname: jenkinsvsc2.example.com,
          target_server_type: "kvm",
          target_server: 135.227.181.233,
          mgmt_ip: 192.168.122.213,
          mgmt_gateway: 192.168.122.1,
          mgmt_netmask_prefix: 24,
          ctrl_ip: 192.168.100.203,
          ctrl_netmask_prefix: 24,
          vsd_fqdn: jenkinsvsd1.example.com,
          system_ip: 1.1.1.3,
          xmpp_username: jenkinsvsc2,
          vsc_static_route_list: { 0.0.0.0/1 } }
    ansible_deployment_host: 135.227.181.233
    mgmt_bridge: "virbr0"
    data_bridge: "virbr1"
    access_bridge: "access"
    images_path: "/var/lib/libvirt/images/"
    ntp_server_list:
      - 135.227.181.232
      - 192.96.202.120
    dns_server_list:
      - 192.168.122.1
      - 128.251.10.145
    dns_domain: example.com
```
