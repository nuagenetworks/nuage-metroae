import os
import subprocess

from charmhelpers.core.hookenv import (
    config,
    log,
    status_set)

from charms.reactive import when, when_not, set_flag
from charmhelpers.core.templating import render

options = config()

CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIR = os.path.join(CHARM_DIR, 'nuage-metro')
VSC_IMAGE_URL = options.get('image_url')
TARGET_SERVER_SSH_KEY_URL = options.get('target_server_ssh_key_url')
IMAGE_DIR = os.path.join(CHARM_DIR, 'images')
VSD_IMAGE_DIR = os.path.join(IMAGE_DIR, 'vsd/qcow2/')
VSD_IMAGE_FILE = os.path.join(VSD_IMAGE_DIR, 'VSD-5.3.3_99.qcow2')
VSC_IMAGE_DIR = os.path.join(IMAGE_DIR, 'vsc/single_disk/')
VSC_IMAGE_FILE = os.path.join(VSC_IMAGE_DIR, 'vsc_singledisk.qcow2')
DEPLOYMENT_DIR = os.path.join(METRO_DIR, "deployments/default")
TEMPLATE_DIR = os.path.join(METRO_DIR, "src/deployment_templates")
PRIVATE_KEY_FILE = "/root/.ssh/id_rsa"
PUBLIC_KEY_FILE = "/root/.ssh/id_rsa.pub"
RELATION_NAME = "container"


@when_not('metroae.installed')
def install_metroae():
    e = 'Installing metroae'
    status_set('active', e)
    log(e)
    install_packages()
    run_shell("virtualenv -p python2.7 .metroaenv")
    run_shell("source .metroaenv/bin/activate && ./metro-setup.sh")

    set_flag("metroae.installed")


@when_not('images.installed')
@when('metroae.installed')
def install_images():
    e = 'Getting VSC resources'
    status_set('active', e)
    log(e)
    pull_images()

    set_flag("images.installed")


def install_packages():
    log("Install packages")
    run_shell("apt-get install -y git wget virtualenv")


def pull_images():
    log("Pull images")
    if not os.path.exists(VSD_IMAGE_DIR):
        os.makedirs(VSD_IMAGE_DIR)

    if not os.path.exists(VSC_IMAGE_DIR):
        os.makedirs(VSC_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSC_IMAGE_URL, VSC_IMAGE_FILE))

    run_shell("wget %s -O %s" % (TARGET_SERVER_SSH_KEY_URL, PRIVATE_KEY_FILE))
    os.chmod(PRIVATE_KEY_FILE, 0o400)


@when_not('config.complete')
@when('host-system.available')
def host_system_avail(juju_info_client):
    e = 'Creating VSC deployment'
    status_set('active', e)
    log(e)

    remote_address = ""

    for conv in juju_info_client.conversations():
        remote_address = conv.get_remote("private-address")

    log(remote_address)

    create_deployment(remote_address)

    set_flag("config.complete")


def create_deployment(target_server_address):
    log("Create deployment")

    run_shell("rm -f " + os.path.join(DEPLOYMENT_DIR, "*"))

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
               'xmpp_tls': "False",
               'openflow_tls': "False",
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
               'vscs': [
                   # VSC 1
                   {
                       'target_server_type': "kvm",
                       'hostname':
                           options.get('vsc_mgmt_ip'),
                       'mgmt_ip':
                           options.get('vsc_mgmt_ip'),
                       'mgmt_ip_prefix':
                           options.get('vsc_mgmt_ip_prefix'),
                       'mgmt_gateway':
                           options.get('vsc_mgmt_gateway'),
                       'ctrl_ip':
                           options.get('vsc_ctrl_ip'),
                       'ctrl_ip_prefix':
                           options.get('vsc_ctrl_ip_prefix'),
                       'system_ip':
                           options.get('vsc_system_ip'),
                       'evpn_neighbor_ip_list':
                           options.get('vsc_evpn_neighbor_ip_list').split(","),
                       'target_server':
                           target_server_address
                   }]},
           config_template=template)

    with open(os.path.join(TEMPLATE_DIR, 'credentials.j2'), "r",
              encoding='utf-8') as f:
        template = f.read()

    render("",
           os.path.join(DEPLOYMENT_DIR, 'credentials.yml'),
           {
               'credentials': [
                   {
                       'name': "default",
                       'target_server_username':
                           options.get('target_server_username')
                   }],
           },
           config_template=template)


@when_not('vsc.deployed')
@when('images.installed', 'config.complete')
def deploy_vsc():
    e = 'Installing VSC'
    status_set('active', e)
    log(e)

    run_shell("source .metroaenv/bin/activate && "
              "HOME=/home/root ./metroae install_vscs "
              "-vvv -e ansible_python_interpreter=python2.7")

    set_flag("vsc.deployed")
    e = 'ready'
    status_set('active', e)
    log(e)


def run_shell(cmd):
    ret = subprocess.Popen(cmd,
                           shell=True,
                           executable='/bin/bash',
                           cwd=METRO_DIR)
    retcode = ret.wait()
    if retcode != 0:
        raise Exception("Non-zero %d return code from %s" % (retcode, cmd))
