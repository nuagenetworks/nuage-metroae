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
/opt/nuage-metro-%{version}
%attr(0755, root, root)
/opt/nuage-metro-%{version}/metro-ansible
/opt/nuage-metro-%{version}/roles/vsd-license/files/vsd_license.py
/opt/nuage-metro-%{version}/roles/vsd-license/files/vsp_base_license.txt
/opt/nuage-metro-%{version}/rpms/metro.spec
/opt/nuage-metro-%{version}/rpms/rpm_build.sh
/opt/nuage-metro-%{version}/scripts/create_zfb_profile.py
/opt/nuage-metro-%{version}/scripts/vrs_verify.py
/opt/nuage-metro-%{version}/scripts/vsc_verify.py
/opt/nuage-metro-%{version}/test/files/archive-ansible
/opt/nuage-metro-%{version}/test/scripts/archive_retriever.sh
/opt/nuage-metro-%{version}/test/scripts/build_incremental.sh
/opt/nuage-metro-%{version}/test/scripts/deploy_all.sh
/opt/nuage-metro-%{version}/test/scripts/deploy_ci.sh
/opt/nuage-metro-%{version}/test/scripts/deploy_ci_all.sh
/opt/nuage-metro-%{version}/test/scripts/deploy_on_esx_ci.sh
/opt/nuage-metro-%{version}/test/scripts/unzip_all.sh
/opt/nuage-metro-%{version}/test/scripts/upgrade_all_ha.sh
/opt/nuage-metro-%{version}/test/scripts/upgrade_all_sa.sh


%pre

%post
# gets executed after installatin of the files
if [ -e /opt/nuage-metro-%{version} ]
then
    pip install -r /opt/nuage-metro-%{version}/rpms/pip-requirements
fi
echo | sh /opt/nuage-metro-%{version}/rpms/VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt --eulas-agreed --regular
