from charms.reactive import when, when_not, set_flag
import subprocess
import os


CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIR = os.path.join(CHARM_DIR, 'nuage-metro')
IMAGE_URL = "http://135.227.146.142/packages/vsp/5.3.3/vsc.tar.gz"
IMAGE_DIR = os.path.join(CHARM_DIR, 'images/vsc/single_disk')
IMAGE_FULL_PATH = os.path.join(IMAGE_DIR, "vsc.tar.gz")


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
    unpack_images()
    create_deployment()

    set_flag("images.installed")


def install_packages():
    run_shell("apt-get install -y git wget")


def pull_images():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    run_shell("wget %s -O %s" % (IMAGE_URL, IMAGE_FULL_PATH))


def unpack_images():
    run_shell("/bin/gunzip " + IMAGE_FULL_PATH)
    run_shell("/bin/tar -xf %s -C %s" % (IMAGE_FULL_PATH.rstrip(".gz"),
                                         IMAGE_DIR))
    os.rename(os.path.join(IMAGE_DIR, "vsc.qcow2"),
              os.path.join(IMAGE_DIR, "vsc_singledisk.qcow2"))


def create_deployment():
    run_shell("rm -rf " + os.path.join(METRO_DIR, "deployments/default"))
    os.rename(os.path.join(CHARM_DIR, "deployment"),
              os.path.join(METRO_DIR, "deployments/default"))


@when_not('vsc.deployed')
@when('images.installed')
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
