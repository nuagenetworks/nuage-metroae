FROM centos:7
COPY yum_requirements.txt /root
COPY pip_requirements.txt /root
#RUN while read l; do yum install -y "$l"; done < /root/yum_requirements.txt
RUN cat /root/yum_requirements.txt | xargs -d '\n' yum install -y
RUN pip3 install -r /root/pip_requirements.txt
WORKDIR /metroae
