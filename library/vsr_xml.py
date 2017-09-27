#!/usr/bin/python
def main():
    module = AnsibleModule(
            argument_spec=(dict(
            vsr_uuid       = dict(required=True, type='str'),
            vsr_name       = dict(required=True, type='str'),
            vsr_memory     = dict(required=True, type='str'),
            vsr_vcpu       = dict(required=True, type='str'),
            mgmt_prefix    = dict(required=True, type='str'),
            mgmt_gateway   = dict(required=True, type='str'),
            vsr_image_path = dict(required=True, type='str'),
            mgmt_port      = dict(required=True, type='str'),
            mgmt_routes    = dict(required=True, type='list'),
            ports          = dict(required=True, type='list'))))
    vsr_uuid       = module.params['vsr_uuid']
    vsr_name       = module.params['vsr_name']
    vsr_memory     = module.params['vsr_memory']
    vsr_vcpu       = module.params['vsr_vcpu']
    mgmt_prefix    = module.params['mgmt_prefix']
    mgmt_gateway   = module.params['mgmt_gateway']
    mgmt_port      = module.params['mgmt_port']
    mgmt_routes    = module.params['mgmt_routes']
    vsr_image_path = module.params['vsr_image_path']
    ports          = module.params['ports']

    try: from xml.etree.ElementTree import Element, SubElement, tostring
    except: module.fail_json(msg="Failed to import xml module")
    else:
        #root object
        domain = Element('domain')
        domain.set('type','kvm')

        uuid = SubElement(domain,'uuid')
        uuid.text = vsr_uuid

        name = SubElement(domain,'name')
        name.text = vsr_name

        # memory definition
        memory = SubElement(domain,'memory')
        memory.set('unit','G')
        memory.text = str(vsr_memory)

        # vcpu definition
        vcpu = SubElement(domain,'vcpu')
        vcpu.text = str(vsr_vcpu)

        # cpu definition
        cpu = SubElement(domain,'cpu')
        cpu.set('mode','host-model')
        cpu_model = SubElement(cpu,'model')
        cpu_model.set('fallback','allow')

        #sysinfo definition
        sysinfo_string = ['slot=A',
                          'chassis=VSR-I',
                          'card=cpm-v',
                          'mda/1=m20-v']
        sysinfo_string += ['address={mgmt_prefix}@active'.format(**locals())]
        for route in mgmt_routes:
            sysinfo_string += ['static-route={route}@{mgmt_gateway}'.format(**locals())]

        sysinfo = SubElement(domain,'sysinfo')
        sysinfo.set('type','smbios')
        sysinfo_system = SubElement(sysinfo,'system')
        sysinfo_system_entry = SubElement(sysinfo_system,'entry')
        sysinfo_system_entry.set('name','product')
        sysinfo_system_entry.text = "TIMOS:{0}".format(' '.join(sysinfo_string))

        # os definition
        os = SubElement(domain,'os')
        os_type = SubElement(os,'type')
        os_type.set('arch','x86_64')
        os_type.set('machine','pc')
        os_type.text = 'hvm'
        os_boot = SubElement(os,'boot')
        os_boot.set('dev','hd')
        os_smbios = SubElement(os,'smbios')
        os_smbios.set('mode','sysinfo')


        #clock definition
        timers = {'pit': ('tickpolicy', 'delay'),
                  'rtc': ('tickpolicy', 'catchup'),
                  'hpet':('present',    'no')}
        def add_timer(name,k,v):
            timer = SubElement(clock, 'timer')
            timer.set('name',name)
            timer.set(k,v)
        clock = SubElement(domain,'clock')
        clock.set('offset','utc')

        for name in timers:
            add_timer(name,
                      timers[name][0],
                      timers[name][1])

        #devices definition
        devices = SubElement(domain,'devices')

        ##emulator for Redhat
        emulator = SubElement(devices,'emulator')
        emulator.text = '/usr/libexec/qemu-kvm'

        #pci controller
        pci_controller = SubElement(devices,'controller')
        pci_controller.set('type','pci')
        pci_controller.set('model','pci-root')

        ##disk part
        disk = SubElement(devices,'disk')
        disk.set('type','file')
        disk.set('device','disk')
        disk_driver = SubElement(disk,'driver')
        disk_driver.set('name','qemu')
        disk_driver.set('type','qcow2')
        disk_driver.set('cache','none')
        disk_src_file = SubElement(disk,'source')
        disk_src_file.set('file',vsr_image_path)
        disk_target = SubElement(disk,'target')
        disk_target.set('dev','hda')
        disk_target.set('bus','virtio')

        ##network part
        def add_interface(bridge):
            interface = SubElement(devices,'interface')
            interface.set('type','bridge')
            interface_src = SubElement(interface,'source')
            interface_src.set('bridge',bridge)
            interface_model = SubElement(interface,'model')
            interface_model.set('type','virtio')
        ##add management interface
        add_interface(mgmt_port)
        ##add mda interfaces
        for _port in ports:
            add_interface(_port)


        # console definition
        serial = SubElement(devices,'serial')
        serial.set('type','pty')
        serial_source = SubElement(serial,'source')
        serial_source.set('path','/dev/pts/1')
        serial_target = SubElement(serial,'target')
        serial_target.set('port','0')
        serial_alias = SubElement(serial,'alias')
        serial_alias.set('name','serial0')

        console = SubElement(devices,'console')
        console.set('type','pty')
        console.set('tty','/dev/pts/1')
        console_source = SubElement(console,'source')
        console_source.set('path','/dev/pts/1')
        console_target = SubElement(console,'target')
        console_target.set('type','serial')
        console_target.set('port','0')
        console_alias = SubElement(console,'alias')
        console_alias.set('name','serial0')

        module.exit_json(changed=True, xml=tostring(domain))
    module.fail_json(msg="Module unexcpected behaviour")

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
