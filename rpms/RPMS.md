# Installing Metro playbooks and dependencies
To install metro rpm package,
1. yum install epel-release
2. yum install metro-2.1.2-1.el7.centos.noarch.rpm 

After the install, rpm will place the nuage code in the /opt/nuage-metro-version folder. Also it will install all the pip dependencies and vmware ovftool.

Now the users can go to /opt/nuage-metro-version/ , update build_vars.yml and run the playbooks. 


To remove metro packages and all dependencies installed, 
1. yum remove metro-2.1.2 
2. yum autoremove
3. pip uninstall –r rpms/pip-requirements

Updated metro code can be downloaded via git clone now or through remove/reinstall of the RPM package.

