#!/bin/bash
set -e
USAGE="Usage: $0 branch (dev or master)"

if [ $# -ne 1 ];
then
    echo "Requires branch (dev or master)"
    echo $USAGE
    exit 1
fi

echo "Create RPM Build Env"
rpmdev-setuptree
cp ./rpms/metro.spec ~/rpmbuild/SPECS/
if [ $1 == 'master' ]
then
    ver=`git describe --tags $(git rev-list --tags --max-count=1)`
    echo "setting rpm version to $ver" 
    sed -i "s/0.0.0/$ver/g" ~/rpmbuild/SPECS/metro.spec
else
    ver="v0.0.0"
fi

mkdir -p ~/rpmbuild/SOURCES/metro-$ver/opt/nuage-metro-$ver/
cp -pR . ~/rpmbuild/SOURCES/metro-$ver/opt/nuage-metro-$ver/
scp root@135.227.181.233:/home/rpm/VMware-ovftool* ~/rpmbuild/SOURCES/metro-$ver/opt/nuage-metro-$ver/rpms
cd  ~/rpmbuild/SOURCES
tar -zcvf metro-$ver.tar.gz metro-$ver/
echo "Completed creating RPM build Env"

echo "Building metro RPM"
cd ~/rpmbuild
rpmbuild -vv -bb SPECS/metro.spec
echo "Completed building RPM"

echo "Copying RPM to FTP server"
if [ $1 == 'master' ]
then
    scp -r ~/rpmbuild/RPMS/noarch/*.rpm rpm@135.227.181.233:/home/rpm/master
else
    scp -r ~/rpmbuild/RPMS/noarch/*.rpm rpm@135.227.181.233:/home/rpm/dev
fi

echo "Completed copying RPM to FTP server"
