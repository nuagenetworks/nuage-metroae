Name: metro          
Version:    0.0.0    
Release:        1%{?dist}
Summary:        Nuage metro packages

License:        GPL
URL:  https://github.com/nuagenetworks/nuage-metro          
Source0:        metro-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot


Requires: epel-release git gcc sshpass openssl-devel 
Requires: python2-pip python-ipaddr python-netaddr python-netifaces python-devel python-devel 
Requires: PyYAML python-jinja2 python-paramiko pycrypto python-setuptools


%description
Metro playbooks and dependencies


%prep
%setup -q


%install
mkdir -p $RPM_BUILD_ROOT
cp -R * $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/nuage-metro-%{version}

%post
# gets executed after installatin of the files
if [ -e /opt/nuage-metro-%{version} ]
then
    pip install -r /opt/nuage-metro-%{version}/rpms/pip-requirements
fi
echo | sh /opt/nuage-metro-%{version}/rpms/VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt --eulas-agreed --regular
