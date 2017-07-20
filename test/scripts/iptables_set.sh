#!/bin/bash
# Sets iptable rules for a given machine.

iptables -t nat -F PREROUTING
iptables -t nat -F POSTROUTING

iptables -t nat -A POSTROUTING -o br-eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -o br-eth1 -j MASQUERADE

gwIP=$(ip addr show br-eth1 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)

removed=${gwIP:9}
mgmtIP=${gwIP:0:9}
incremented=$(($removed+110))
dataGW="${mgmtIP}0"
mgmtIP="${mgmtIP}$incremented"

# VSD1
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

# VSC1
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

# VSC2
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

# VSTAT1
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

# VNSUTILS1
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP

mgmtIP=${mgmtIP:0:9}
incremented=$(($incremented+10))
mgmtIP="${mgmtIP}$incremented"

# NSGV
iptables -t nat -A PREROUTING -s $gwIP -j DNAT --to $mgmtIP
iptables -t nat -A POSTROUTING -s $mgmtIP -j SNAT --to-source $gwIP
