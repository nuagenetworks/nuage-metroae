import os
import subprocess

from charmhelpers.core.hookenv import (
    config,
    log,
    related_units,
    relation_get,
    relation_ids,
    status_set)

from charms.reactive import when, when_not, set_flag
from charmhelpers.core.templating import render

options = config()

CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIR = os.path.join(CHARM_DIR, 'nuage-metro')
VSD_IMAGE_URL = "http://135.227.146.142/packages/juju/VSD-5.3.3_99.qcow2"
VSC_IMAGE_URL = options.get('image_url')
# VSC_IMAGE_URL = "http://135.227.146.142/packages/juju/vsc_singledisk.qcow2"
KEY_URL = "http://135.227.146.142/packages/juju/id_rsa"
PUBLIC_KEY_URL = "http://135.227.146.142/packages/juju/id_rsa.pub"
IMAGE_DIR = os.path.join(CHARM_DIR, 'images')
VSD_IMAGE_DIR = os.path.join(IMAGE_DIR, 'vsd/qcow2/')
VSD_IMAGE_FILE = os.path.join(VSD_IMAGE_DIR, 'VSD-5.3.3_99.qcow2')
VSC_IMAGE_DIR = os.path.join(IMAGE_DIR, 'vsc/single_disk/')
VSC_IMAGE_FILE = os.path.join(VSC_IMAGE_DIR, 'vsc_singledisk.qcow2')
DEPLOYMENT_DIR = os.path.join(METRO_DIR, "deployments/default")
TEMPLATE_DIR = os.path.join(METRO_DIR, "src/deployment_templates")
KEY_FILE = "/root/.ssh/id_rsa"
PUBLIC_KEY_FILE = "/root/.ssh/id_rsa.pub"
RELATION_NAME = "container"


@when_not('metroae.installed')
def install_metroae():
    e = 'Installing metroae'
    log("Install metroae")
    install_packages()
    run_shell("virtualenv -p python2.7 .metroaenv")
    run_shell("source .metroaenv/bin/activate && ./metro-setup.sh")

    set_flag("metroae.installed")
    status_set('active', e)


@when_not('images.installed')
@when('metroae.installed')
def install_images():
    log("Install images")
    pull_images()
    # create_deployment()

    set_flag("images.installed")


def install_packages():
    log("Install packages")
    run_shell("apt-get install -y git wget virtualenv")


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


@when_not('config.complete')
# @when('container.connected')
@when('config.changed')
def create_deployment():
    log("Create deployment")

    # target_server = get_target_server()
    # if target_server is None:
    #     exit(0)

    # log(target_server)
    # set_flag("config.complete")

    # return

    run_shell("rm -f " + os.path.join(DEPLOYMENT_DIR, "*"))

    SOURCE_DIR = os.path.join(CHARM_DIR, "deployment")

    run_shell("cp %s %s" % (os.path.join(SOURCE_DIR, "vsds.yml"),
                            DEPLOYMENT_DIR))
    # run_shell("cp %s %s" % (os.path.join(SOURCE_DIR, "vscs.yml"),
    #                         DEPLOYMENT_DIR))

    with open(os.path.join(TEMPLATE_DIR, 'common.j2'), "r",
              encoding='utf-8') as f:
        template = f.read()

    render("",
           os.path.join(DEPLOYMENT_DIR, 'common.yml'),
           {
               'nuage_unzipped_files_dir':
                   IMAGE_DIR,
               'user_ssh_pub_key':
                   PUBLIC_KEY_FILE,
               'vsd_fallocate_size_gb': 10,
               'vsd_ram': 8,
               'dns_domain':
                   options.get('dns_domain'),
               'vsd_fqdn_global':
                   options.get('vsd_fqdn_global'),
               'mgmt_bridge':
                   options.get('mgmt_bridge'),
               'data_bridge':
                   options.get('data_bridge'),
               'ntp_server_list':
                   options.get('ntp_server_list').split(","),
               'dns_server_list':
                   options.get('dns_server_list').split(",")},
           config_template=template)

    with open(os.path.join(TEMPLATE_DIR, 'vscs.j2'), "r",
              encoding='utf-8') as f:
        template = f.read()

    render("",
           os.path.join(DEPLOYMENT_DIR, 'vscs.yml'),
           {
               'nuage_unzipped_files_dir':
                   IMAGE_DIR,
               'user_ssh_pub_key':
                   PUBLIC_KEY_FILE,
               'vscs': [
                   # VSC 1
                   {
                       'target_server_type': "kvm",
                       'hostname':
                           options.get('vsc1_hostname'),
                       'mgmt_ip':
                           options.get('vsc1_mgmt_ip'),
                       'mgmt_ip_prefix':
                           options.get('vsc1_mgmt_ip_prefix'),
                       'mgmt_gateway':
                           options.get('vsc1_mgmt_gateway'),
                       'ctrl_ip':
                           options.get('vsc1_ctrl_ip'),
                       'ctrl_ip_prefix':
                           options.get('vsc1_ctrl_ip_prefix'),
                       'system_ip':
                           options.get('vsc1_system_ip'),
                       'target_server':
                           options.get('vsc1_target_server')
                   },
                   # VSC 2
                   {
                       'target_server_type': "kvm",
                       'hostname':
                           options.get('vsc2_hostname'),
                       'mgmt_ip':
                           options.get('vsc2_mgmt_ip'),
                       'mgmt_ip_prefix':
                           options.get('vsc2_mgmt_ip_prefix'),
                       'mgmt_gateway':
                           options.get('vsc2_mgmt_gateway'),
                       'ctrl_ip':
                           options.get('vsc2_ctrl_ip'),
                       'ctrl_ip_prefix':
                           options.get('vsc2_ctrl_ip_prefix'),
                       'system_ip':
                           options.get('vsc2_system_ip'),
                       'target_server':
                           options.get('vsc2_target_server')}]},
           config_template=template)

    set_flag("config.complete")


def get_target_server():
    rel_ids = relation_ids(RELATION_NAME)
    if len(rel_ids) == 0:
        log("Relation not created yet")
        return None
    rel_id = rel_ids[0]
    units = related_units(rel_id)
    unit = units[0]
    return relation_get(attribute="private-address",
                        unit=unit,
                        rid=rel_id)


# @when_not('vsd.deployed')
# @when('start')
# def deploy_vsd():
#     log("Deploy VSD")
#     run_shell("source .metroaenv/bin/activate && "
#               "HOME=/home/root ./metroae install_vsds "
#               "-vvv -e ansible_python_interpreter=python2.7")
#     set_flag("vsd.deployed")


@when_not('vsc.deployed')
# @when('vsd.deployed')
@when('start')
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
