from charms.reactive import when, when_not, set_flag
from charms import ansible
import subprocess

@when('ansible.available')
@when_not('metroae.installed')
def do_something():
    ret = subprocess.Popen("./metro-setup.sh",
            shell=True,
            executable='/bin/bash',
            cwd='./nuage-metro/')
    retcode = ret.wait()
    if retcode != 0:
        raise Exception("Non-zero return code from metro-setup.sh")
    set_flag("metroae.installed")
    ansible.apply_playbook('playbook.yaml')
