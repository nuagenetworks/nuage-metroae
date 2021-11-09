FROM centos:7
COPY yum_requirements.txt /root
COPY pip_requirements.txt /root
RUN cat /root/yum_requirements.txt | xargs -d '\n' yum install -y
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN pip3 install -r /root/pip_requirements.txt
ENV LC_ALL=en_US.utf8
WORKDIR /metroae
