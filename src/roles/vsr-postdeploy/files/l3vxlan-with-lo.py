from alc import dyn

# example of metadata to be added in VSD WAN Service:
# "rd=3:3,vprnAS=65000,vprnRD=65000:1,vprnRT=target:65000:1,vprnLo=1.1.1.1"

# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l3dom1" type vrf-vxlan action setup policy "py-vrf-vxlan" vni 1234 rt-i target:3:3 rt-e target:3:3 metadata "rd=3:3,vprnAS=65000,vprnRD=65000:1,vprnRT=target:65000:1,vprnLo=1.1.1.1"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l3dom1" type vrf-vxlan action teardown policy
# "py-vrf-vxlan" vni 1234 rt-i target:3:3 rt-e target:3:3


def setup_script(vsdParams):

    print("These are the VSD params: " + str(vsdParams))
    servicetype = vsdParams['servicetype']
    vni = vsdParams['vni']
    rt = vsdParams['rt']

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
        print(
            'servicetype, VPLS id, rt, vni, rd, VPRN id, vprn_AS, vprn_RD, vprn_RT, vprn_Lo:',
            servicetype,
            vplsSvc_id,
            rt,
            vni,
            rd,
            vprnSvc_id,
            vprn_AS,
            vprn_RD,
            vprn_RT,
            vprn_Lo)
        dyn.add_cli("""

        configure service
           vpls %(vplsSvc_id)s customer 1 name l3-backhaul-vpls%(vplsSvc_id)s create
              allow-ip-int-bind vxlan-ipv4-tep-ecmp
                 exit
              description vpls%(vplsSvc_id)s
              bgp
                 route-distinguisher %(rd)s
                 route-target %(rt)s
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
              autonomous-system %(vprn_AS)s
              route-distinguisher %(vprn_RD)s
              auto-bind-tunnel resolution any
              vrf-target %(vprn_RT)s
              interface "vpls-%(vplsSvc_id)s" create
                 vpls "vpls%(vplsSvc_id)s" evpn-tunnel
                 exit
              interface "lo1" create
                 address %(vprn_Lo)s/32
                 loopback
                 exit
              no shutdown
              exit
        exit

      """ % {'vplsSvc_id': vplsSvc_id, 'vprnSvc_id': vprnSvc_id, 'vni': vsdParams['vni'], 'rt': rt, 'rd': metadata['rd'], 'vprn_AS': vprn_AS, 'vprn_RD': vprn_RD, 'vprn_RT': vprn_RT, 'vprn_Lo': vprn_Lo})
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
            'vprn_Lo': vprn_Lo}

# ------------------------------------------------------------------------------------------------


def teardown_script(setupParams):
    print("These are the teardown_script setupParams: " + str(setupParams))
    servicetype = setupParams['servicetype']
    if servicetype == "VRF-VXLAN":
        print("Test1")
        print("These are the teardown_script setupParams: " + str(setupParams))
        dyn.add_cli("""
        configure service
            vpls %(vplsSvc_id)s
               bgp-evpn
                   vxlan
                       shut
                       exit
                   no evi
                   exit
               no vxlan vni %(vni)s
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
               shutdown
            exit
        no vprn %(vprnSvc_id)s
        exit

      """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vprnSvc_id': setupParams['vprnSvc_id'], 'vni': setupParams['vni']})
        return setupParams


d = {"script": (setup_script, None, None, teardown_script)}

dyn.action(d)
