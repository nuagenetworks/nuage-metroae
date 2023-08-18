from alc import dyn
# example of metadata to be added in VSD WAN Service: "rd=1:1"
# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l2dom1" type l2-domain action setup policy "py-l2" vni 1234 rt-i target:1:1 rt-e target:1:1 metadata "rd=1:1"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l2dom1" type l2-domain action teardown policy "py-l2" vni
# 1234 rt-i target:1:1 rt-e target:1:1


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
    # vprnSvc_id = dyn.select_free_id("service-id")
    print("this are the free svc ids picked up by the system: VPLS:" + vplsSvc_id)

    if servicetype == "L2DOMAIN":
        rd = metadata['rd']
        # vprn_AS = metadata ['vprnAS']
        # vprn_RD = metadata ['vprnRD']
        # vprn_RT = metadata ['vprnRT']
        # vprn_Lo = metadata ['vprnLo']
        # irb_GW = metadata ['irbGW']
        print('servicetype, VPLS id, rt, vni, rd',
              servicetype, vplsSvc_id, rt, vni, rd)
        dyn.add_cli("""
        configure service
          vpls %(vplsSvc_id)s customer 1 name vpls%(vplsSvc_id)s create
          description vpls%(vplsSvc_id)s
          proxy-arp
            dynamic-arp-populate
            no shutdown
          exit
          bgp
            route-distinguisher %(rd)s
            route-target %(rt)s
            pw-template-binding 1 import-rt %(rt)s
            exit
          exit
          vxlan vni %(vni)s create
          exit
          bgp-ad
            vpls-id %(rd)s
            no shut
          exit
          bgp-evpn
            evi %(vplsSvc_id)s
            vxlan
              no shut
            exit
          exit
          no shutdown
          exit
          exit
        exit
        """ % {'vplsSvc_id': vplsSvc_id, 'vni': vsdParams['vni'], 'rt': rt, 'rd': metadata['rd'], })
# L2DOMAIN returns setupParams: vplsSvc_id, vprnSvc_id, servicetype, vni
        return {'vplsSvc_id': vplsSvc_id,
                'servicetype': servicetype, 'vni': vni}
# ------------------------------------------------------------------------------------------------


def teardown_script(setupParams):
    print("These are the teardown_script setupParams: " + str(setupParams))
    servicetype = setupParams['servicetype']
    if servicetype == "L2DOMAIN":
        dyn.add_cli("""
        configure service
        vpls %(vplsSvc_id)s
        no description
        proxy-arp shut
        no proxy-arp
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
        bgp-ad
        shutdown
        exit
        no bgp-ad
        no bgp
        no bgp-evpn
        shutdown
        exit
        no vpls %(vplsSvc_id)s
        exit
        exit
        """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vni': setupParams['vni']})
        return setupParams


d = {"script": (setup_script, None, None, teardown_script)}
dyn.action(d)
