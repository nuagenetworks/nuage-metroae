Name: metro          
Version:    v0.0.0    
Release:        1%{?dist}
Summary:        Nuage metro packages

License:        GPL
URL:  https://github.com/nuagenetworks/nuage-metro          
Source0:        metro-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot


Requires: git gcc sshpass openssl-devel libvirt-client
Requires: python2-pip python-ipaddr python-netaddr python-netifaces python-devel python-devel 
Requires: PyYAML python-jinja2 python-paramiko pycrypto python-setuptools

%description
Metro playbooks and dependencies

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT
cp -pR * $RPM_BUILD_ROOT
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
/opt/nuage-metro-%{version}/roles
/opt/nuage-metro-%{version}/Docker
/opt/nuage-metro-%{version}/callback_plugins
/opt/nuage-metro-%{version}/filter_plugins
/opt/nuage-metro-%{version}/examples
/opt/nuage-metro-%{version}/library
/opt/nuage-metro-%{version}/test/files
/opt/nuage-metro-%{version}/test/nuage_unzip
/opt/nuage-metro-%{version}/test/archive_retriever
/opt/nuage-metro-%{version}/.git
/opt/nuage-metro-%{version}/.gitignore
/opt/nuage-metro-%{version}/.mailmap
/opt/nuage-metro-%{version}/*.md
/opt/nuage-metro-%{version}/*.yml
/opt/nuage-metro-%{version}/*.cfg
/opt/nuage-metro-%{version}/rpms
/opt/nuage-metro-%{version}/scripts/vars


%attr(0755,root,root)
/opt/nuage-metro-%{version}/test/scripts/*.*
/opt/nuage-metro-%{version}/scripts/*.*
/opt/nuage-metro-%{version}/metro-ansible

%pre

%post
# gets executed after installatin of the files
if [ -e /opt/nuage-metro-%{version} ]
then
    pip install -r /opt/nuage-metro-%{version}/rpms/pip-requirements
fi
echo | sh /opt/nuage-metro-%{version}/rpms/VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt --eulas-agreed --regular
