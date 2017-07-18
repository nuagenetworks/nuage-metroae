FROM centos

ENTRYPOINT ["/ecStart.sh"]
CMD [""]

RUN yum install -y epel-release && yum update -y && \
    yum install -y python python-devel python-pip sshpass git gcc libssl2-dev libffi-devel python-devel openssl-devel && \
    pip install ansible==2.2.2 netmiko netaddr && \
    yum clean all && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config

# ARG git_user=your_user_name
# ARG git_password=xxxxxxx
# RUN git clone https://$git_user:$git_password@github.com/nuagenetworks/nuage-metro.git && \
#    sed -i 's|build_vars.yml|/files/build_vars.yml|g' nuage-metro/build.yml

ADD nuage-metro /nuage-metro

ADD ecStart.sh /
