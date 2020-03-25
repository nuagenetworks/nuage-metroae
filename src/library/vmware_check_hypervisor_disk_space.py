import requests
import sys
from ansible.module_utils.basic import AnsibleModule
from pyVmomi import vim, vmodl
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
        host = vm.name
        return host
        # host = vm.runtime.host
        # if host is not None:
        #    return host.name

    return None


def get_connection(ip_addr, user, password, port, validate_certs):
    if validate_certs:
        connection = SmartConnect(
            host=ip_addr, port=port, user=user, pwd=password)
    else:
        connection = SmartConnectNoSSL(
            host=ip_addr, port=port, user=user, pwd=password)
    return connection


def get_available_disk_space(esxi_host_name, conn, disk_check_args, user, pwd, file_path):
    obj = None
    content = conn.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    for c in container.view:
        if c.name == esxi_host_name:
            obj = c
            break
    vm = obj
    creds = vim.vm.guest.NamePasswordAuthentication(username=user, password=pwd)
    pm = content.guestOperationsManager.processManager
    ps = vim.vm.guest.ProcessManager.ProgramSpec(
      programPath="/usr/bin/df",
      arguments=disk_check_args
    )

    res = pm.StartProgram(vm, creds, ps)

    result_file = content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(vm, creds, file_path)

    results = requests.get(result_file.url, verify=False)

    disk_space_check_results = results.content

    content.guestOperationsManager.fileManager.DeleteFileInGest(vm, creds, file_path)

    return disk_space_check_results


def main():
    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(
                type='str',
                default=os.environ.get('VMWARE_HOST')
            ),
            username=dict(
                type='str',
                default=os.environ.get('VMWARE_USER')
            ),
            password=dict(
                type='str', no_log=True,
                default=os.environ.get('VMWARE_PASSWORD')
            ),
            validate_certs=dict(required=False, type='bool', default=True),
            uuid=dict(required=False, type='str'),
            port=dict(required=False, type=int, default=443),
            required_available_space=dict(required=True, type=int),
            disk_space_path=dict(required=True, type='str')
        ),
    )

    ip_addr = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    uuid = module.params['uuid']
    required_space = module.params['required_available_space']
    path = module.params['disk_space_path']

    try:
        connection = get_connection(ip_addr, username, password, port, validate_certs)

        if connection is None:
            module.fail_json(msg="Establishing connection to %s failed" % ip_addr)

        esxi_host = get_esxi_host(ip_addr, port, username, password, uuid, validate_certs)

        if esxi_host is None:
            module.fail_json(msg="Could not find ESXi host using uuid %s" % uuid)

        file_path = "/tmp/req_space"
        disk_check_args = "{0} | tail -n 1 | awk '{print $4}' > {1}".format(str(path), str(file_path))

        available_disk_space = get_available_disk_space(esxi_host, connection, disk_check_args, username, password, file_path)

        required_space_kb = (float(required_space) * 1024 * 1024)

        if float(available_disk_space) > required_space_kb:
          print("Sufficient disk space: {0}".format(float(available_disk_space)))
        else:
          print("Insufficent disk space: {0}. Need at least {1}".format(float(available_disk_space), required_space_kb)

    except Exception as e:
        module.fail_json(msg="Could not get available disk space: %s" % str(e))


if __name__ == "__main__":
    main()
