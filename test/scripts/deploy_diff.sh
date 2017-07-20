#!/bin/bash
set -e

USAGE="Usage: $0 version"

if [ $# -ne 4 ];
then
    echo "Requires exactly 2 arguments"
    echo $USAGE
    exit 1
fi

if [ $1 = 3.2.R10 ];
then
    sed -i  "/vns_operations_list:/,/nsgv_mac: '52:54:00:88:85:12' }/ d" test/files/build_vars_all.yml
fi

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
cp ./test/files/zfb.yml .

# Get IP address of server on which script is being run
IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

# Does not touch the netmask as we assume 0/24 prefix

# The following "sed" commands populate the build_vars.yml file with
# the correct mgmt IP addresses for the following naming convention:
# if the hypervisor's given Jen-BackEnd IP is 10.106.1.7, the mgmt IP for:
# VSD1 will be 10.106.1.117
# VSC1 will be 10.106.1.127
# VSC2 will be 10.106.1.137
# VSTAT1 will be 10.106.1.147
# VNSUTIL1 will be 10.106.1.157

# If given the hypervisor's Jen-BackEnd IP, the first machine will be given
# an IP of the correct subnet, and the final number in the IP address will
# be incremented by 110 from the initial Jen-BackEnd IP.

# Every sequential machine after the first will increment by only 10 as 
# shown in the example above.

# The hypervisor's given Jen-BackEnd IP will be the mgmt gateway and the 
# dns server given to the VSD.

# With each sed for each VM, the correct iptables entries
# have been added to ensure connection to the VMs
# *iptables entries commented out for ctrl & data planes

# Previous iptables entries for PREROUTING and 
# POSTROUTING are flushed before new entries
# are added to the iptables

iptables -t nat -F PREROUTING
iptables -t nat -F POSTROUTING

# Allowing these masquerades must be the first route added
# otherwise the precedence will not work correctly.

iptables -t nat -A POSTROUTING -o br-eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -o br-eth1 -j MASQUERADE

#gwIP=$(ip addr show br-eth1 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)

gwIP=$4

removed=${gwIP:9}
mgmtIP=${gwIP:0:9}
incremented=$(($removed+110))
dataGW="${mgmtIP}0"
mgmtIP="${mgmtIP}$incremented"

sed -i "s/MGMT_GATEWAY/$gwIP/g" roles/reset-build/files/build_vars.yml
sed -i "s/DNS_VSD/$gwIP/g" roles/reset-build/files/build_vars.yml
sed -i "s/DATA_GATEWAY/$dataGW/g" roles/reset-build/files/build_vars.yml
sed -i "s/VSD1_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml
sed -i "s/VSD1/$mgmtIP/g" zfb.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

# The following is for HA deployments only.

if [ $2 = "ha" ];
then
    sed -i "18,29 s/^#//" roles/reset-build/files/build_vars.yml
    mgmtIP=${mgmtIP:0:9}
    incremented=$(($incremented+10))
    mgmtIP="${mgmtIP}$incremented"

    sed -i "s/VSD2_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

    iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
    iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

    mgmtIP=${mgmtIP:0:9}
    incremented=$(($incremented+10))
    mgmtIP="${mgmtIP}$incremented"

    sed -i "s/VSD3_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

    iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
    iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP
fi

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VSC1_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml
sed -i "s/VSC1/$mgmtIP/g" zfb.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VSC2_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml
sed -i "s/VSC2/$mgmtIP/g" zfb.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VSTAT1_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

# The following conditional is for HA deployments only

if [ $2 = "ha" ];
then
    sed -i "s/GLOBAL_VSD_FQDN/xmpp.example.com/g" roles/reset-build/files/build_vars.yml

    sed -i "85,99 s/^#//" roles/reset-build/files/build_vars.yml

    mgmtIP=${mgmtIP:0:9}
    incremented=$(($incremented+10))
    mgmtIP="${mgmtIP}$incremented"

    sed -i "s/VSTAT2_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

    iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
    iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

    mgmtIP=${mgmtIP:0:9}
    incremented=$(($incremented+10))
    mgmtIP="${mgmtIP}$incremented"

    sed -i "s/VSTAT3_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

    iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
    iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP
fi

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VNSUTIL1_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/NSGV_IP/$mgmtIP/g" roles/reset-build/files/build_vars.yml

iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VSC1_CTRL/$mgmtIP/g" roles/reset-build/files/build_vars.yml

#iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
#iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VSC2_CTRL/$mgmtIP/g" roles/reset-build/files/build_vars.yml

#iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
#iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

sed -i "s/VNSUTIL1_DATA/$mgmtIP/g" roles/reset-build/files/build_vars.yml

#iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
#iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

IPADDR=$3

sed -i "s/GLOBAL_VSD_FQDN/jenkinsvsd1.example.com/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/ENVIRONMENT_TYPE/$2/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
sed -i "s/SERVER_TYPE/kvm/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv
