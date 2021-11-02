FROM centos:7
COPY yum_requirements.txt /root
COPY pip_requirements.txt /root
RUN while read l; do yum install -y "$l"; done < /root/yum_requirements.txt
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install -r /root/pip_requirements.txt
WORKDIR /metroae
