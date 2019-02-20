from charms.reactive import when, when_not, set_flag
import subprocess
import os
from charmhelpers.core.hookenv import log
from charmhelpers.core.hookenv import status_set


CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIR = os.path.join(CHARM_DIR, 'nuage-metro')
VSD_IMAGE_URL = "http://135.227.146.142/packages/juju/VSD-5.3.3_99.qcow2"
VSC_IMAGE_URL = "http://135.227.146.142/packages/juju/vsc_singledisk.qcow2"
KEY_URL = "http://135.227.146.142/packages/juju/id_rsa"
PUBLIC_KEY_URL = "http://135.227.146.142/packages/juju/id_rsa.pub"
VSD_IMAGE_DIR = os.path.join(CHARM_DIR, 'images/vsd/qcow2/')
VSD_IMAGE_FILE = os.path.join(VSD_IMAGE_DIR, 'VSD-5.3.3_99.qcow2')
VSC_IMAGE_DIR = os.path.join(CHARM_DIR, 'images/vsc/single_disk/')
VSC_IMAGE_FILE = os.path.join(VSC_IMAGE_DIR, 'vsc_singledisk.qcow2')
KEY_FILE = "/root/.ssh/id_rsa"
PUBLIC_KEY_FILE = "/root/.ssh/id_rsa.pub"


@when_not('metroae.installed')
def install_metroae():
    e = 'Installing metroae'
    log("Install metroae")
    #run_shell("virtualenv -p python2.7 .metroaenv")
    #run_shell("source .metroaenv/bin/activate && ./metro-setup.sh")
    #set_flag("metroae.installed")
    status_set('active', e)


@when_not('images.installed')
@when('metroae.installed')
def install_images():
    log("Install images")
    install_packages()
    pull_images()
    create_deployment()

    set_flag("images.installed")


def install_packages():
    log("Install packages")
    run_shell("apt-get install -y git wget")


def pull_images():
    log("Pull images")
    if not os.path.exists(VSD_IMAGE_DIR):
        os.makedirs(VSD_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSD_IMAGE_URL, VSD_IMAGE_FILE))

    if not os.path.exists(VSC_IMAGE_DIR):
        os.makedirs(VSC_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSC_IMAGE_URL, VSC_IMAGE_FILE))

    run_shell("wget %s -O %s" % (KEY_URL, KEY_FILE))
    os.chmod(KEY_FILE, 0o400)

    run_shell("wget %s -O %s" % (PUBLIC_KEY_URL, PUBLIC_KEY_FILE))


def create_deployment():
    log("Create deployment")
    SOURCE_DIR = os.path.join(METRO_DIR, "../deployment")
    TARGET_DIR = os.path.join(METRO_DIR, "deployments/default")
    run_shell("rm -rf " + TARGET_DIR)
    run_shell("mkdir " + TARGET_DIR)
    run_shell("cp " + SOURCE_DIR + "/* " + TARGET_DIR)


@when_not('vsd.deployed')
@when('images.installed')
def deploy_vsd():
    log("Deploy VSD")
    run_shell("source .metroaenv/bin/activate && "
              "HOME=/home/root ./metroae install_vsds "
              "-vvv -e ansible_python_interpreter=python2.7")
    set_flag("vsd.deployed")


@when_not('vsc.deployed')
@when('vsd.deployed')
def deploy_vsc():
    log("Deploy VSC")
    run_shell("source .metroaenv/bin/activate && "
              "HOME=/home/root ./metroae install_vscs "
              "-vvv -e ansible_python_interpreter=python2.7")
    set_flag("vsc.deployed")


def run_shell(cmd):
    ret = subprocess.Popen(cmd,
                           shell=True,
                           executable='/bin/bash',
                           cwd=METRO_DIR)
    retcode = ret.wait()
    if retcode != 0:
        raise Exception("Non-zero %d return code from %s" % (retcode, cmd))
