FROM centos

ENTRYPOINT ["/ecStart.sh"]
CMD [""]

RUN yum install -y epel-release && yum update -y && \
    yum install -y python python-devel python-pip sshpass git gcc libssl2-dev libffi-devel python-devel openssl-devel python-netaddr python-dns && \
    pip install ansible==2.3 netmiko pexpect && \
    yum clean all && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD nuage-metro/Docker/ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config

# ARG git_user=jbemmel
# ARG git_password=xxxx

# ADD vspk.tar.gz /tmp
# RUN cd /tmp/vspk-5.0.2.32 && python ./setup.py install

# RUN git clone https://$git_user:$git_password@github.com/nuagenetworks/nuage-metro.git && \
#    sed -i 's|build_vars.yml|/files/build_vars.yml|g' nuage-metro/build.yml
ADD nuage-metro /nuage-metro

ADD nuage-metro/Docker/ecStart.sh /
