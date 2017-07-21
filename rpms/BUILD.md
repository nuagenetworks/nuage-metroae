# RPM Build environment setup

## Prerequisites

You will need to make sure certain prerequisite packages are installed on your build server. On el7, this can be accomplished with the following command:

`sudo yum install -y rpmdevtools rpmlint`

You will also need to clone the Metro repo to your local workspace. The sample commands shown herein assume that you are working from the 'root' of your clone.

## Create Environment

### Setup Tree

Once the packages are installed, you create an rpm build environment in your home directory with the following command:

`rpmdev-setuptree`

This will create a rpmbuild directory tree inside your home directory.

```
[caso@jen-docker-slave1 ~]$ ls rpmbuild/
BUILD  BUILDROOT  RPMS  SOURCES  SPECS  SRPMS
```

### Populate `SPECS`

From your clone of the Metro repo, copy the RPM specification file into the `SPECS` directory.

`cp ./rpms/metro.spec ~/rpmbuild/SPECS/`

After copying, edit the `metro.spec` file and replace the version with whatever version you want to use for this build.

### Populate `SOURCES`

Create a directory and copy Metro into it. Note that you should use the same version in the path that you have used in the `metro.spec` file.

`mkdir -p ~/rpmbuild/SOURCES/metro-0.0.0/opt/nuage-metro-0.0.0/`

`cp -pR . ~/rpmbuild/SOURCES/metro-0.0.0/opt/nuage-metro-0.0.0/`

Note that the portion of the path after `metro-0.0.0` is the same path that the code will be installed to on the target system. In this case, that will be:

```
/opt/metro-0.0.0/
```

### Get ovstool

ovstool should be copied into the Metro `SOURCES` directory. You can retrieve it from any location you wish. For our example, we will use a local NFS server in our lab:

`scp root@135.227.181.233:/home/rpm/VMware-ovftool* ~/rpmbuild/SOURCES/metro-$ver/opt/nuage-metro-0.0.0/rpms`

### Create tarball

Metro sources must be tarred before the build.

```
cd  ~/rpmbuild/SOURCES
tar -zcvf metro-$ver.tar.gz metro-$ver/
```

## Build RPM

Change to the `rpmbuild` directory and execute the build.

```
cd ~/rpmbuild
rpmbuild -vv -bb SPECS/metro.spec
```

The new RPM will be available here:

```
ls ~/rpmbuild/RPMS/noarch/*.rpm
```

## RPM Specification Details

The file `./rpms/metro.spec` controls many of the details for the build. Here are sample contents:

```
Name: metro          
Version:    v0.0.0    
Release:        1%{?dist}
Summary:        Nuage metro packages

License:        GPL
URL:  https://github.com/nuagenetworks/nuage-metro          
Source0:        metro-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot

Requires: git gcc sshpass openssl-devel
Requires: python2-pip python-ipaddr python-netaddr python-netifaces python-devel python-devel
Requires: PyYAML python-jinja2 python-paramiko pycrypto python-setuptools

%description
Metro playbooks and dependencies

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT
cp -R * $RPM_BUILD_ROOT
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/nuage-metro-%{version}

%pre

%post
# gets executed after installatin of the files
if [ -e /opt/nuage-metro-%{version} ]
then
    pip install -r /opt/nuage-metro-%{version}/rpms/pip-requirements
fi
echo | sh /opt/nuage-metro-%{version}/rpms/VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt --eulas-agreed --regular
```

### Spec file notes

- `Version` corresponds to the Metro version being built into the RPM. In general, builds from the dev branch will always be `0.0.0` whereas builds from the master branch will be labeled with the real Metro version.
- `Requires` holds a list of packages that Metro depends on. These packages will be installed on the deployment host when the RPM is installed. Multiple `Requires` specifications are supported.
- `%post` corresponds to actions that get executed on the deployment host after the RPM installation is complete. We use this section to install `pip` and any packages that are not part of `Requires`, e.g. vspk, netmiko, and ansible itself. The packages to be installed using pip are listed in:

`./rpms/pip-requirements`

## Automated RPM builds with Jenkins

There are two types of Jenkins jobs to build metro RPMs, regular Jenkins freestyle jobs and Jenkins declarative pipeline. Freestyle jobs run one or more scripts that are specified in the configuration details for a single job. Pipeline jobs are described in a Jenkins file and execute in stages.

### Jenkins freestyle jobs: RPM_Build_Dev and RPM_Build_Master

The follow launches an rpm build on the dev branch:

`./rpms/rpm_build.sh dev`

Dev branch will always have a single rpm build labeled version v0.0.0.

For master branch:

`./rpms/rpm_build.sh master`

Master branch will get the version number from the release tag.

The following is used to get the latest tag for the master branch for the purpose of rpm naming:

`git describe --tags $(git rev-list --tags --max-count=1)`

Note that the following line in jenkinsfile or inside jenkins pipeline script needs to be changed to run as a different user:

```
git url: "https://github.com/wasanthag/nuage-metro.git", branch: 'master', credentialsId: 'wasanthag'
```

The credentialsId can be found under Jenkins credentials.

### Jenkins declarative pipelines: RPM_dev_PL

These jobs have configuration read from the rpms/jenkinsfile or alternatively copy/paste the same jenkinsfile content in to inline pipeline script text area in the job itself.

Caveats :
1.    Jenkins node that runs build jobs must be setup with keyless ssh access to the ftp server (135.227.181.233). This allows Jenkins shell scripts to copy the built RPM files to the ftp server as well as get the VMware OVF tool. Currently, Jenkins jobs are scheduled on the BM server cs2-009 with a label rpm_build.
2.    Jenkins jobs for creating automated builds should be run as caso or any other user having a home directory and logging shell. This is due to the fact rpm build process needs to create directory and run shell commands.
3.    Sometimes rpmbuilds folder on Jenkins server may need to be reset to user/group of caso with chown –R caso.caso ~/rpmbuilds
4.    Sometimes home/rpm folder on ftp server may need to be set chmod –R 755 /home/rpm
