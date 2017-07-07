Name: metro          
Version:    2.1.2    
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
/opt/nuage-metro-2.1.2

