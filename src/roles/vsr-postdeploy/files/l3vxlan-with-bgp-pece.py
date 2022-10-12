# Metadata example
#
# rd=3:3,vprnAS=65000,vprnRD=65000:1002,vprnRT=target:65000:1002,vprnLo=1.1.1.1,customer=pepsi,customeras=64555,customerip=2.2.2.2,customerpass=password,customersubnet=192.168.1.0/31,customersap=1/1/1:10


from alc import dyn

# example of metadata to be added in VSD WAN Service:
# "rd=3:3,vprnAS=65000,vprnRD=65000:1,vprnRT=target:65000:1,vprnLo=1.1.1.1,customer=pepsi,customeras=640001,customerip=2.2.2.2,customerpass=password,customersubnet=192.168.1.0/31,customersap=1.1.1:10"

# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l3dom1" type vrf-vxlan action setup policy "py-vrf-vxlan" vni 1234 rt-i target:3:3 rt-e target:3:3 metadata "rd=3:3,vprnAS=65000,vprnRD=65000:1,vprnRT=target:65000:1,vprnLo=1.1.1.1"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l3dom1" type vrf-vxlan action teardown policy
# "py-vrf-vxlan" vni 1234 rt-i target:3:3 rt-e target:3:3


def setup_script(vsdParams):

    print("These are the VSD params: " + str(vsdParams))
    servicetype = vsdParams.get('servicetype')
    vni = vsdParams.get('vni')
    rt = vsdParams.get('rt')

# add "target:" if provisioned by VSD (VSD uses x:x format whereas tools
# command uses target:x:x format)
    if not rt.startswith('target'):
        rt = "target:" + rt

    metadata = vsdParams['metadata']

# remove trailing space at the end of the metadata
    metadata = metadata.rstrip()

    print("VSD metadata" + str(metadata))
    metadata = dict(e.split('=') for e in metadata.split(','))
    print("Modified metadata" + str(metadata))
    vplsSvc_id = dyn.select_free_id("service-id")
    vprnSvc_id = dyn.select_free_id("service-id")
    print("this are the free svc ids picked up by the system: VPLS:" +
           vplsSvc_id + " + VPRN:" + vprnSvc_id)

    if servicetype == "VRF-VXLAN":

        rd = metadata['rd']
        vprn_AS = metadata['vprnAS']
        vprn_RD = metadata['vprnRD']
        vprn_RT = metadata['vprnRT']
        vprn_Lo = metadata['vprnLo']
        customer = metadata['customer']
        customeras = metadata['customeras']
        customerip = metadata['customerip']
        customerpass = metadata['customerpass']
        customersubnet = metadata['customersubnet']
        customersap = metadata['customersap']
        print(
            'servicetype, VPLS id, rt, vni, rd, VPRN id, vprn_AS, vprn_RD, vprn_RT, vprn_Lo, customer, customeras, customerip, customerpass, customersubnet, customersap:',
            servicetype,
            vplsSvc_id,
            rt,
            vni,
            rd,
            vprnSvc_id,
            vprn_AS,
            vprn_RD,
            vprn_RT,
            vprn_Lo,
            customer,
            customeras,
            customerip,
            customerpass,
            customersubnet,
            customersap)
        dyn.add_cli("""
        configure router policy-options
           begin
             community _VSD_%(vplsSvc_id)s members %(rt)s
             policy-statement vsi_import_%(vplsSvc_id)s
                entry 10
                   from
                      family evpn
                      community _VSD_%(vplsSvc_id)s
                      exit
                   action accept
                   exit
                exit
             exit
             policy-statement vsi_export_%(vplsSvc_id)s
                entry 10
                   from
                      family evpn
                      exit
                      action accept
                      community add _VSD_%(vplsSvc_id)s
                      exit
                   exit
              exit
           commit
        exit

        configure service
           vpls %(vplsSvc_id)s customer 1  name l3-backhaul-vpls%(vplsSvc_id)s create
              allow-ip-int-bind vxlan-ipv4-tep-ecmp
                 exit
              description vpls%(vplsSvc_id)s
              bgp
                 route-distinguisher %(rd)s
                 vsi-import vsi_import_%(vplsSvc_id)s
                 vsi-export vsi_export_%(vplsSvc_id)s
                 exit
              vxlan vni %(vni)s create
                 exit
              bgp-evpn
                 ip-route-advertisement
                 vxlan
                     no shut
                     exit
                 exit
              no shutdown
              exit
            exit
        exit


        configure service
           vprn %(vprnSvc_id)s customer 1 create
              auto-bind-tunnel resolution any
              router-id %(vprn_Lo)s
              autonomous-system %(vprn_AS)s
              route-distinguisher %(vprn_RD)s
              vrf-target %(vprn_RT)s
              interface "vpls-%(vplsSvc_id)s" create
                 vpls "vpls%(vplsSvc_id)s" evpn-tunnel
                 exit
              interface "lo1" create
                 address %(vprn_Lo)s/32
                 loopback
                 exit
              no shutdown
              interface %(customer)s create
                address %(customersubnet)s
                sap %(customersap)s create
                exit
             exit
              bgp group %(customer)s
                 peer-as %(customeras)s
                 neighbor %(customerip)s authentication-key %(customerpass)s
             exit
        exit

      """ % {'vplsSvc_id': vplsSvc_id, 'vprnSvc_id': vprnSvc_id, 'vni': vsdParams['vni'], 'rt': rt, 'rd': metadata['rd'], 'vprn_AS': vprn_AS, 'vprn_RD': vprn_RD, 'vprn_RT': vprn_RT, 'vprn_Lo': vprn_Lo, 'customer': customer, 'customeras': customeras, 'customerip': customerip, 'customerpass': customerpass, 'customersubnet': customersubnet, 'customersap': customersap})
        # VRF-VXLAN returns setupParams: vplsSvc_id, vprnSvc_id, servicetype,
        # vni, vprn_AS, vprn_RD, vprn_RT, vprn_Lo
        return {
            'vplsSvc_id': vplsSvc_id,
            'vprnSvc_id': vprnSvc_id,
            'servicetype': servicetype,
            'vni': vni,
            'vprn_AS': vprn_AS,
            'vprn_RD': vprn_RD,
            'vprn_RT': vprn_RT,
            'vprn_Lo': vprn_Lo,
            'customer': customer,
            'customeras': customeras,
            'customerip': customerip,
            'customerpass': customerpass,
            'customersubnet': customersubnet,
            'customersap': customersap}

# ------------------------------------------------------------------------------------------------


def teardown_script(setupParams):
    print("These are the teardown_script setupParams: " + str(setupParams))
    servicetype = setupParams.get('servicetype')
    if servicetype == "VRF-VXLAN":
        dyn.add_cli("""
        configure service
            vpls %(vplsSvc_id)s
               no description
               bgp-evpn
                   vxlan
                       shut
                       exit
                   no evi
                   exit
               no vxlan vni %(vni)s
               bgp
                  no route-distinguisher
                  no route-target
                  exit
               no bgp
               no bgp-evpn
               shutdown
               exit
            no vpls %(vplsSvc_id)s
            vprn %(vprnSvc_id)s
               interface lo1 shutdown
               no interface lo1
               interface "vpls-%(vplsSvc_id)s"
                  vpls "vpls%(vplsSvc_id)s"
                     no evpn-tunnel
                     exit
                  no vpls
                  shutdown
                  exit
               no interface "vpls-%(vplsSvc_id)s"
               interface %(customer)s create
                    sap %(customersap)s shutdown
                    no sap %(customersap)s
                 shutdown
                 exit
               no interface %(customer)s
               bgp shutdown
               no bgp
               shutdown
            exit
        no vprn %(vprnSvc_id)s
        exit
        configure router policy-options
            begin
            no community _VSD_%(vplsSvc_id)s
            no policy-statement vsi_import_%(vplsSvc_id)s
            no policy-statement vsi_export_%(vplsSvc_id)s
            commit
        exit

      """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vprnSvc_id': setupParams['vprnSvc_id'], 'vni': setupParams['vni'], 'customer': setupParams['customer'], 'customersap': setupParams['customersap']})
        return setupParams


d = {"script": (setup_script, None, None, teardown_script)}

dyn.action(d)
