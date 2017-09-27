nuage_unzip
===========

unarchive distro and put files to structured folder tree.

Role variables
=========
for this role 2 variables should be defined in `build_vars.yml`:
- `nuage_zipped_files_dir` - defines absolute path to folder where all zip archive stored
- `nuage_unzipped_files_dir` - defines absolute path to folder where unarchived files will be store in structure tree during role execution.

Note: no need run `./metro-ansible build.yml` as variables from `build_vars.yml` will be imported explicitly.

Example Playbook
================
```
---
- hosts: "{{ nuage_unzip_targets | default('localhost') }}"
  gather_facts: yes
  vars:
    unzip_user: root
  pre_tasks:
    - name: Include build variable files
      include_vars: "{{ build_vars_file | default ('build_vars.yml') }}"
      tags:
        - always
  roles:
    - nuage-unzip
```

How to use tags
===============
To unpack only specific components of Nuage distribution, specific tags can be used.
To list all supported tags:
```bash
nuage-metro]$ ./metro-ansible nuage_unzip.yml --list-tags

playbook: nuage_unzip.yml

  play #1 (localhost): localhost	TAGS: []
      TASK TAGS: [always, libnetwork, nuage_os, vns, vrs, vsc, vsd, vsr, vstat]

```

To run unpack of VSD only use tag `vsd`:
```bash
nuage-metro]$ ./metro-ansible nuage_unzip.yml -t vsd
```
