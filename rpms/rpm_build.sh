#!/bin/bash
echo "Create RPM Build Env"
rpmdev-setuptree
pwd
cp ./rpms/metro.spec ~/rpmbuild/SPECS/
mkdir -p ~/rpmbuild/SOURCES/metro-2.1.2/opt/nuage-metro-2.1.2/
cp -R . ~/rpmbuild/SOURCES/metro-2.1.2/opt/nuage-metro-2.1.2/
cd  ~/rpmbuild/SOURCES
tar -zcvf metro-2.1.2.tar.gz metro-2.1.2/
echo "Completed creating RPM build Env"

pwd
echo "Building metro RPM"
cd ~/rpmbuild
rpmbuild -vv -bb SPECS/metro.spec
echo "Completed creating RPM"

cp -r ~/rpmbuild/RPMS/*.rpm /home/caso/nfs-data/misc/
