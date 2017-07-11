#!/bin/bash
echo "Create RPM Build Env"
rpmdev-setuptree 
cp ./rpms/metro.spec ~/rpmbuild/SPECS/
mkdir -p ~/rpmbuild/SOURCES/metro-2.1.2/opt/nuage-metro-2.1.2/
cp -r . ~/rpmbuild/SOURCES/metro-2.1.2/opt/nuage-metro-2.1.2/
tar -zcvf ~/rpmbuild/SOURCES/metro-2.1.2.tar.gz ~/rpmbuild/SOURCES/metro-2.1.2
echo "Completed creating RPM build Env"

echo "Building metro RPM"
rpmbuild -v -bb ~/rpmbuild/SPECS/metro.spec
echo "Completed creating RPM"

cp -r ~/rpmbuild/RPMS/*.rpm /home/caso/nfs-data/misc/


