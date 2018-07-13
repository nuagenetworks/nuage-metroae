#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import re

Documentation = '''

----
module: autostart_vm
short_description: Change autostart settings for vcenter vms
options:
  name: 
    description: 'Name of the VM'
    required: true
    aliases: ["vm"]
  enabled:
    description: 'Whether or not to start VM on host startup'
    required: true
    aliases: ["autostart"]
  order:
    description: 'Relative startup order of VMs. If a VM already occupies this spot, it will be shifted down. List is sequential and VMs are numbered starting at 1.
                  By default, VMs are added to the end of the startup list.'
    required: false
  skip:
    description: 'Skip unregistered VMs' 
    default: false
  state:
    description: 'Whether or not the VM should be running now. Default behavior is to not change state.
    required: false
    choices: ["start", "stop"]
'''

EXAMPLES = '''
# Enable autostart for test-vm-1
- autostart_vm:
  name: test-vm-1
  
# Disable autostart for test-vm-1
- autostart_vm:
  name: test-vm-1
  enabled: false

# Enable autostart for test-vm-1 at specific position
- autostart_vm:
  name: test-vm-1
  order: 1
'''

COMMAND_LIST = {
  'get_vms': 'vim-cmd vmsvc/getallvms',
  'get_autostart_seq': 'vim-cmd hostsvc/autostartmanager/get_autostartseq',
  'enable_start': 'vim-cmd hostsvc/autostartmanager/update_autostartentry ' +
                  '{vim_id} "PowerOn" "10" "{order}" ' +
                  '"guestShutdown" "systemDefault" "systemDefault"',
  'disable_start': 'vim-cmd hostsvc/autostartmanager/update_autostartentry -- ' +
                   '"{vim_id}" "PowerOff" "1" "-1" ' +
                   '"guestShutdown" "systemDefault" "systemDefault"'
} 

class VmMgr(object):
  """ manages autostart entries """
  def __init__(self, module):
    self.module = module
    self.params = self.module.params
    self.check_mode = module.check_mode
    self.commands = COMMAND_LIST
    self.vmname_to_id = self.load_vms
    self.vm_startup_info = self.load_startuplist
  
  def load_vms(self):
    vms = dict()
    cmd = self.commands['get_vms']
    rc, out, err = self.module.run_command(cmd)
    if rc != 0:
      self.module.fail_json(msg="Unable to get list of vms",
                            cmd=cmd,
                            rc=rc,
                            stdout=out,
                            stderr=err)
    for line in out.split('\n'):
      if line.startswith('Vmid') or line == '':
        continue
      if not re.match(r'^\d+ +\S+ +\[S+\] \S+/\S+\.vmx', line):
        continue
      fields = line.split()
      vms[fields[1]] = int(fields[0])
    return vms

  def load_startuplist(self):
    startup_info = dict()
    vm_id = 0
    cmd = self.commands['get_autostart_seq']
    rc, out, err = self.module.run_command(cmd)
    if rc != 0:
      self.module.fail_json(msg="Unable to get autostart sequence",
                            rc=rc,
                            cmd=cmd,
                            stdout=out,
                            stderr=err)
    for line in out.split('\n'):
      if line.lstrip().startswith(('(', '}', ']')) or line == '':
        continue
      (key, _, val) = line.strip("', \n").strip().split()
      if key == 'key':
        vm_id = int(val.split(":")[1])
        startup_info[vm_id] = {}
      elif key == 'startOrder':
        startup_info[vm_id]['order'] = int(val)
      elif key == 'startAction':
        startup_info[vm_id]['action'] = val.strip('"')
    return startup_info
  
  def update_vm(self):
    vm_name = self.params['name']
    new_start_rule = self.params['enabled']
    new_order = self.params['order']

    if vm_name not in self.vmname_to_id:
      if self.params['skip']:
        return(False, "VM %s not found, skipping" % vm_name, {})
      else:
        self.module.fail_json(msg="VM not found",
                              rc=-1)
    
    vm_id = self.vmname_to_id[vm_name]
    enable_start_cmd = self.commands['enable_start']
    diable_start_cmd = self.commands['disable_start']

    command = None
    changed = False
    ret_msg = 'passed'
    ret_params = {'vm_id': vm_id}

    if not new_start_rule:
      if vm_id in self.vm_startup_info:
        prev_order = self.vm_startup_info[vm_id]['order']
        prev_action = self.vm_startup_info[vm_id]['action']
        if prev_action != "PowerOff":
          changed = True
          ret_msg = "autostart is disabled, moved to -1"
          command = diable_start_cmd.format(vm_id = vm_id)
          ret_params['prev_action'] = prev_action
        else:
          ret_msg = "autostart already disabled"
      else:
        ret_msg = "autostart already disabled"
    else:
      if vm_id in self.vm_startup_info:
        prev_order = self.vm_startup_info[vm_id]['order']
        prev_action = self.vm_startup_info[vm_id]['action']
        if prev_action != "PowerOn" or prev_order == -1:
          changed = True
          if new_order is None:
            new_order = len([v for v in self.vm_startup_info.values() if v['order'] > 0]) + 1 
          ret_msg = "autostart enabled at %d" % new_order
          ret_params['prev_action'] = prev_action
          ret_params['prev_pos'] = prev_order
          ret_params['new_pos'] = new_order
          command = enable_start_cmd.format(vm_id = vm_id, order = new_order)
        if new_order is not None and new_order != prev_order and not changed:
          changed = True
          command = enable_start_cmd.format(vm_id = vm_id, order = new_order)
          ret_msg = "autostart enabled, VM moved from %d to %d" % (prev_order, new_order)
          ret_params['prev_pos'] = prev_order
          ret_params['new_pos'] = new_order
        if not changed:
          ret_msg = "autostart already enabled for %s in position %d" % (vm_name, prev_order)
      else:
        changed = True
        if new_order is None:
          new_order = len([v for v in self.vm_startup_info.values() if v['order'] > 0]) + 1
        command = enable_start_cmd.format(vm_id = vm_id, order = new_order)
        ret_msg = "autostart enabled for %s at position %d" % (vm_name, new_order)
        ret_params['new_pos'] = new_order
    if command is not None:
        ret_params['command'] = command
        if not self.check_mode:
          rc, out, err = self.module.run_command(command)
          if rc != 0:
            self.module.fail_json(msg="Cannot make changes",
                                  rc=rc,
                                  cmd=command,
                                  stdout=out,
                                  stderr=err)
    return (changed, ret_msg, ret_params)

        

def main():
    arg_spec = dict(
      name = dict(aliases=['vm'], required=True),
      enabled = dict(aliases=['autostart'], required=False, type='bool', default=True),
      skip = dict(required=False, type='bool', default=False)    
    )
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    manager = VmMgr(module)
    changed, msg, params = manager.update_vm()
    module.exit_json(changed=changed, msg=msg, **params)


main()




