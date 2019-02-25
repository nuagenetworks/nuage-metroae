import fcntl
import os
import socket
import struct
import subprocess

from charmhelpers.core.hookenv import (
    config,
    Hooks,
    log,
    related_units,
    relation_get,
    relation_ids,
    relation_set,
    status_set)

from charms.reactive import when, when_not, set_flag
from charmhelpers.core.templating import render

hooks = Hooks()

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

    # run_shell("wget %s -O %s" % (VSD_IMAGE_URL, VSD_IMAGE_FILE))

    if not os.path.exists(VSC_IMAGE_DIR):
        os.makedirs(VSC_IMAGE_DIR)

    run_shell("wget %s -O %s" % (VSC_IMAGE_URL, VSC_IMAGE_FILE))

    run_shell("wget %s -O %s" % (TARGET_SERVER_SSH_KEY_URL, PRIVATE_KEY_FILE))
    os.chmod(PRIVATE_KEY_FILE, 0o400)


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
                       'target_server':
                           get_ip_address(options.get('vsc_target_server_interface'))
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
                           options.get('vsc_target_server_username')
                   }],
           },
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


@when_not('vsc.deployed')
@when('config.complete')
def deploy_vsc():
    log("Deploy VSC")
    run_shell("source .metroaenv/bin/activate && "
              "HOME=/home/root ./metroae install_vscs "
              "-vvv -e ansible_python_interpreter=python2.7")
    set_flag("vsc.deployed")


@hooks.hook('vrs-controller-service-relation-broken')
def vrs_controller_service_broken(rid=None):
    log("vrs_controller_service_broken")
    log(rid)


@hooks.hook('vrs-controller-service-relation-changed')
def vrs_controller_service_changed(rid=None):
    log("vrs_controller_service_changed")
    log(rid)


@hooks.hook('vrs-controller-service-relation-departed')
def vrs_controller_service_departed(rid=None):
    log("vrs_controller_service_departed")
    log(rid)


@hooks.hook('vrs-controller-service-relation-joined')
def vrs_controller_joined(rid=None):
    global vsc_mgmt_ip
    log("vrs_controller_joined")
    log(rid)
    vsc_mgmt_ip = options.get('vsc_mgmt_ip')
    settings = {
        'vsc-ip-address': vm_ip_address
    }
    relation_set(relation_id=rid, **settings)


@hooks.hook('container-relation-broken')
def container_broken(rid=None):
    log("container_broken")
    log(rid)


@hooks.hook('container-relation-changed')
def container_changed(rid=None):
    global hypervisor_ip
    log("container_changed")
    log(rid)
    units = related_units(rid)
    unit = units[0]
    hypervisor_ip = relation_get(attribute="private-address",
                                 unit=unit,
                                 rid=rid)
    log("Found ip")
    log(hypervisor_ip)


@hooks.hook('container-relation-departed')
def container_departed(rid=None):
    log("container_departed")
    log(rid)


@hooks.hook('container-relation-joined')
def container_joined(rid=None):
    global hypervisor_ip
    log("container_joined")
    log(rid)
    units = related_units(rid)
    unit = units[0]
    hypervisor_ip = relation_get(attribute="private-address",
                                 unit=unit,
                                 rid=rid)
    log("Found ip")
    log(hypervisor_ip)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def run_shell(cmd):
    ret = subprocess.Popen(cmd,
                           shell=True,
                           executable='/bin/bash',
                           cwd=METRO_DIR)
    retcode = ret.wait()
    if retcode != 0:
        raise Exception("Non-zero %d return code from %s" % (retcode, cmd))
