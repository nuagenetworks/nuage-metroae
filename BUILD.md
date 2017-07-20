# build and reset-build playbooks

The build playbook (`build.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-ansible build.yml` will use the variables defined in `build_vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build.yml` playbook will do all the work for you.

Note that the syntax of the contents of `build_vars.yml` must be precise. If things get messed up, we have provided the `reset_build.yml` playbook to let you start over. *When you run `./metro-ansible rest_build.yml`, the contents of `build_vars.yml` will be overwritten, the `hosts` file will be destroyed, the `host_vars` directory will be destroyed, and the `group_vars` directory will be destroyed. The variable configuration of metro will be reset to factory settings! You may lose your work!* A backup copy of `build_vars.yml` will be created with a proper timestamp in case you did not mean it.

To run the build, execute:

`ansible-playbook build.yml`

or

`./metro-ansible build.yml`

To reset the build to factory settings, execute:

`ansible-playbook reset_build.yml`

or

`./metro-ansible reset_build.yml`

# nuage_unzip.yml playbook

When the `build.yml` playbook is executed, it expects to find unzipped Nuage software files (QCOW2, OVA, and Linux Package files) for items that are being upgraded or installed. You can either copy the proper files to their locations, shown below, or you can use the nuage_unzip.yml playbook to do the work for you. Simply specify the proper source and target directories in `build_vars.yml`:
```
nuage_zipped_files_dir: "<your_path_with_zipped_software>"
nuage_unzipped_files_dir: "<your_path_for_unzipped_software>"
```
and run `./metro-ansible nuage_unzip.yml` playbook to do the heavy lifting.

Here are the expected paths to binaries. Binaries that are not required need not have a path here.

```
<your_path>/vsd/qcow2/ (or <your_path>/vsd/ova/ for VMware)
<your_path>/vsc/
<your_path>/vrs/el7/
<your_path>/vrs/u14_04/
<your_path>/vrs/u16_04/
<your_path>/vrs/vmware/
<your_path>/vrs/hyperv/
<your_path>/vstat/
<your_path>/vns/nsg/
<your_path>/vns/util/
```

