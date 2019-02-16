from charms.reactive import when, when_not, set_flag
import subprocess
import os


CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIR = os.path.join(CHARM_DIR, 'nuage-metro')
VSD_IMAGE_URL = "http://135.227.146.142/packages/juju/VSD-5.3.3_99.qcow2"
VSC_IMAGE_URL = "http://135.227.146.142/packages/juju/vsc_singledisk.qcow2"
DEPLOYMENT_URL = "http://135.227.146.142/packages/juju/deployment.tar.gz"
KEY_URL = "http://135.227.146.142/packages/juju/id_rsa"
VSD_IMAGE_DIR = os.path.join(CHARM_DIR, 'images/vsd/qcow2/')
VSD_IMAGE_FILE = os.path.join(VSD_IMAGE_DIR, 'VSD-5.3.3_99.qcow2')
VSC_IMAGE_DIR = os.path.join(CHARM_DIR, 'images/vsc/single_disk/')
VSC_IMAGE_FILE = os.path.join(VSC_IMAGE_DIR, 'vsc_singledisk.qcow2')
DEPLOYMENT_FILE = os.path.join(CHARM_DIR, 'deployment.tar.gz')
KEY_FILE = "/root/.ssh/id_rsa"


@when_not('metroae.installed')
def install_metroae():
    run_shell("virtualenv -p python2.7 .metroaenv")
    run_shell("source .metroaenv/bin/activate && ./metro-setup.sh")
    set_flag("metroae.installed")


@when_not('images.installed')
@when('metroae.installed')
def install_images():
    install_packages()
    pull_images()
    create_deployment()

    set_flag("images.installed")


def install_packages():
    run_shell("apt-get install -y git wget")


def pull_images():
    if not os.path.exists(VSD_IMAGE_DIR):
        os.makedirs(VSD_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSD_IMAGE_URL, VSD_IMAGE_FILE))

    if not os.path.exists(VSC_IMAGE_DIR):
        os.makedirs(VSC_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSC_IMAGE_URL, VSC_IMAGE_FILE))

    run_shell("wget %s -O %s" % (DEPLOYMENT_URL, DEPLOYMENT_FILE))

    run_shell("wget %s -O %s" % (KEY_URL, KEY_FILE))
<<<<<<< HEAD
    os.chmod(KEY_FILE, 0o400)
=======
    os.chmod(KEY_FILE, 0400)
>>>>>>> 8973e941ed5c50f5e61f7e9b4b07e5a8647951e9


def create_deployment():
    run_shell("gunzip " + DEPLOYMENT_FILE)
    run_shell("tar -xvf " + os.path.join(CHARM_DIR, "deployment.tar"))
    run_shell("rm -rf " + os.path.join(METRO_DIR, "deployments/default"))
    run_shell("rm -rf " + os.path.join(METRO_DIR, "deployments/default"))
    os.rename(os.path.join(CHARM_DIR, "deployment"),
              os.path.join(METRO_DIR, "deployments/default"))


@when_not('vsd.deployed')
@when('images.installed')
def deploy_vsd():
    run_shell("source .metroaenv/bin/activate && "
              "HOME=/home/root ./metroae install_vsds "
              "-vvv -e ansible_python_interpreter=python2.7")
    set_flag("vsd.deployed")


@when_not('vsc.deployed')
@when('vsd.deployed')
def deploy_vsc():
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
