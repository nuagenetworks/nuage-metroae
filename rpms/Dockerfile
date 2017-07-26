FROM centos


RUN yum install -y epel-release && yum update -y && \
    yum install -y python python-requests python-pip sshpass git gcc libssl2-dev libffi-devel python-devel openssl-devel && \
    pip install --upgrade pip && \
    pip install pexpect ansible==2.2.1 netmiko netaddr vspk pyvmomi pysphere && \
    yum clean all && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ADD nuage-metro /opt/nuage-metro
COPY VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt  /tmp

RUN /tmp/VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle.txt --eulas-agreed --regula

