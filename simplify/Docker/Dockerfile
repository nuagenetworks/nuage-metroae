FROM centos

ENTRYPOINT ["/ecStart.sh"]
CMD [""]

RUN yum install -y epel-release && yum update -y && \
    yum install -y python python-devel python-pip sshpass git gcc libssl2-dev libffi-devel python-devel openssl-devel python-netaddr python-dns python-jmespath unzip && \
    curl -sL https://rpm.nodesource.com/setup_8.x | bash - && yum install -y nodejs && \ 
    pip install ansible==2.4 netmiko netaddr pexpect && \
    mkdir -p /root/.ansible && cd /root/.ansible && \
    npm i superagent agentkeepalive netmask express netmask body-parser multer && \
    yum clean all && rm -rf /var/cache/yum /tmp/* /var/tmp/*

ADD simplify/Docker/ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config

ADD simplify /simplify
ADD simplify/Docker/ecStart.sh /

RUN sed -i 's/{,3}(/{,3}>?(/g' /usr/lib/python2.7/site-packages/ansible/plugins/terminal/sros.py && rm -f /usr/lib/python2.7/site-packages/ansible/plugins/terminal/sros.pyc
