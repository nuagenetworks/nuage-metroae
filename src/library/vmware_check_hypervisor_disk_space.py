import subprocess
from ansible.module_utils.basic import AnsibleModule
import sys
from pyVmomi import vim
from pyVim.connect import SmartConnect
from pyVim.connect import SmartConnectNoSSL
sys.dont_write_bytecode = True

DOCUMENTATION = '''

'''

EXAMPLES = '''

'''

def get_esxi_host(ip_addr, port, username, password, id, validate_certs):
    uuid = id
    si = get_connection(ip_addr, username, password, port, validate_certs)
    vm = si.content.searchIndex.FindByUuid(None,
                                           uuid,
                                           True,
                                           False)
    if vm is not None:
        host = vm.runtime.host
        if host is not None:
            return host.name

    return None

def get_connection(ip_addr, user, password, port, validate_certs):
    if validate_certs:
        connection = SmartConnect(
            host=ip_addr, port=port, user=user, pwd=password)
    else:
        connection = SmartConnectNoSSL(
            host=ip_addr, port=port, user=user, pwd=password)
    return connection

def get_host_obj(esxi_host_name, conn, disk_check_args, user, pwd):
    obj = None
    content = conn.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    for c in container.view:
        if c.name == host_name:
            obj = c
            break
    creds = vim.vm.guest.NamePasswordAuthentication(username=user, password=pwd)
    pm = content.guestOperationsManager.processManager
    ps = vim.vm.guest.ProcessManager.ProgramSpec(
      programPath="/usr/bin/df",
      arguments=disk_check_args
    )

    res = pm.StartProgram(obj, creds, ps)

def check_available_disk_space(host_name, connection):
    host_obj = get_host_obj(host_name, connection)
    if host_obj is None:
      return {'failed': True, 'msg': 'Could not find {0} in list of hosts'.format(host_name)}
