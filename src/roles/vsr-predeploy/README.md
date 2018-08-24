vsr-predeploy
=============

supported mode of deployment:
- integrated

for virtual NIC ports `virtio` driver will be configured

from installation guide
=======================
Although the integrated VSR model is easy to deploy, it may be necessary to deploy multiple integrated model VSR systems to achieve scale or redundancy for a specific application.
From a configuration perspective, an integrated VSR is modeled as a chassis with one slot. The slot is equipped with the cpm-v card type that maps one-to-one with the VM. The VSR displays a chassis type of VSR-I.
When a cpm-v card is installed in the VSR-I chassis, it loads the both.tim software image, which presents the view that the VSR-I system has two slots:
an “A” slot running control plane and management tasks
a “1” slot running datapath tasks
In a VSR-I system, Slot “1” has four MDA slots that are numbered 1 through 4. Each MDA slot can be equipped with any of the supported VSR MDAs described in Section  3.5.2 subject to the following limitations:
Maximum of four 20-port I/O MDAs
Maximum of 1 virtualized ISA-AA
Maximum of 1 virtualized ISA-BB
Maximum of 1 virtualized ISA-tunnel



Allocation of vCPUs for Control and Management Tasks
==============================================================
The number of vCPUs available for control and management plane tasks (such as OSPF, BGP, and SNMP) depends on the system configuration.
VSR-I System Configuration
In a VSR-I system, the number of cores available for both CPM control and IOM control functions defaults to one.
In cases where an ISA is installed and the VM has a total of three or more vCPUs, the default number of control cores is two. However, more vCPUs can be reserved for the control plane by using the control-cpu-cores SMBIOS parameter. See section 6.4.8 for more information about control-cpu-cores and other SMBIOS parameters.




vsr networking
==============
In the VirtIO model, the virtual NIC port is internally connected to a logical interface within the host. The logical host interface may map directly to a physical NIC port/VLAN or it may connect to a vSwitch within the host. If a vNIC port is connected to a vSwitch, a physical NIC port/VLAN must be added as a bridge port of the vSwitch to enable traffic to reach other hosts.

vsr-i requierements from release notes
======================================
VSR-I Requirements
The VM of an integrated-mode VSR has the following configuration and resource requirements:
• Minimum of 2-8 vCPU cores for any VSR-I depending on the application (see section 4.4).
Maximum number of usable vCPU cores is 22.
• Minimum 4GB, 8GB, 16GB, 20GB or 30GB of vRAM memory (backed by 1GB huge pages)
depending on the application (see section 4.5). Maximum usable memory is 64GB.
• In a multi-socket system supporting NUMA the vCPUs and vRAM of the VSR-I VM should
be allocated from one single NUMA node, and this should also be the NUMA node
associated with the SR-IOV and PCI pass-through NIC ports used by the VM. This may
require CPU pinning in the definition of the guest. To understand the NUMA topology of
the system you can use numactl --hardware or virsh capabilities and the NUMA node
association of eth0 (for example) can be read from
/sys/class/net/eth0/device/numa_node.
• The vhost-net threads should be pinned to vCPU cores not used by any virtual VSR
machine (using the 'emulatorpin’ setting).
• UUID must match the one requested in the license
• SMBIOS may indicate chassis=VSR-I card=cpm-v mda=m20-v but these are the default
values.
• VM must be assigned 1+N virtual interfaces, where N=0-15. The first virtual interface
(lowest PCI bus/device/function address) must be VirtIO. The next N virtual interfaces
can be any combination of VirtIO, SR-IOV and PCI pass-through


release notes for release 15.0.R1
https://infoproducts.alcatel-lucent.com/aces/cgi-bin/dbaccessfilename.cgi/3HE120920001TQZZA_V1_VSR%2015.0.R1%20Software%20Release%20Notes.pdf

installation guide for release 15
https://infocenter.alcatel-lucent.com/private/VSR150R1/index.jsp?topic=/com.vsr.isg/html/getting_started_vsr.html
