from alc import dyn

# example of metadata to be added in VSD WAN Service on PE1: "vprnRD=65000:1,vprnRT=target:65000:100,irbGW=10.2.2.1/24,vrrpID=1,vrrpIP=10.2.2.254,vrrpPRIO=150"
# example of metadata to be added in VSD WAN Service on PE2:
# "vprnRD=65000:2,vprnRT=target:65000:100,irbGW=10.2.2.2/24,vrrpID=1,vrrpIP=10.2.2.254,vrrpPRIO=100"

# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l2domIRB1-red" type l2-domain-irb action setup policy "py-l2-irb-red" vni 1234 rt-i target:2:2 rt-e target:2:2 metadata "vprnRD=65000:1,vprnRT=target:65000:100,irbGW=10.2.2.1/24,vrrpID=1,vrrpIP=10.2.2.254,vrrpPRIO=150"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l2domIRB1-red" type l2-domain-irb action teardown policy
# "py-l2-irb-red" vni 1234 rt-i target:2:2  rt-e target:2:2


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

    if servicetype == "L2DOMAIN-IRB":
        vprn_RD = metadata['vprnRD']
        vprn_RT = metadata['vprnRT']
        irb_GW = metadata['irbGW']
        vrrp_ID = metadata['vrrpID']
        vrrp_IP = metadata['vrrpIP']
        vrrp_PRIO = metadata['vrrpPRIO']
        print(
            'servicetype, VPLS id, rt, vni, VPRN id, vprn_RD, vprn_RT, irb_GW, vrrp_ID, vrrp_IP, vrrp_PRIO:',
            servicetype,
            vplsSvc_id,
            rt,
            vni,
            vprnSvc_id,
            vprn_RD,
            vprn_RT,
            irb_GW,
            vrrp_ID,
            vrrp_IP,
            vrrp_PRIO)
        dyn.add_cli("""
        configure service
           vpls %(vplsSvc_id)s customer 1 name vpls%(vplsSvc_id)s create
              allow-ip-int-bind vxlan-ipv4-tep-ecmp
              exit
              description vpls%(vplsSvc_id)s
              bgp
                 route-target %(rt)s
              exit
              vxlan vni %(vni)s create
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
        configure service
           vprn %(vprnSvc_id)s customer 1 create
              auto-bind-tunnel resolution any
              route-distinguisher %(vprn_RD)s
              vrf-target %(vprn_RT)s
              interface "irbvpls-%(vplsSvc_id)s" create
                 address %(irb_GW)s
                 vrrp %(vrrp_ID)s
                     priority %(vrrp_PRIO)s
                     backup %(vrrp_IP)s
                     ping-reply
                 exit
                 vpls "vpls%(vplsSvc_id)s"
                 exit
              exit
              no shutdown
           exit
        exit

      """ % {'vplsSvc_id': vplsSvc_id, 'vprnSvc_id': vprnSvc_id, 'vni': vsdParams['vni'], 'rt': rt, 'vprn_RD': vprn_RD, 'vprn_RT': vprn_RT, 'irb_GW': irb_GW, 'vrrp_ID': vrrp_ID, 'vrrp_IP': vrrp_IP, 'vrrp_PRIO': vrrp_PRIO})
        # L2DOMAIN-IRB returns setupParams: vplsSvc_id, vprnSvc_id,
        # servicetype, vni, vprn_RD, vprn_RT, irb_GW, vrrp_ID, vrrp_IP,
        # vrrp_PRIO
        return {
            'vplsSvc_id': vplsSvc_id,
            'vprnSvc_id': vprnSvc_id,
            'servicetype': servicetype,
            'vni': vni,
            'vprn_RD': vprn_RD,
            'vprn_RT': vprn_RT,
            'irb_GW': irb_GW,
            'vrrp_ID': vrrp_ID,
            'vrrp_IP': vrrp_IP,
            'vrrp_PRIO': vrrp_PRIO}

# ------------------------------------------------------------------------------------------------


def teardown_script(setupParams):
    print("These are the teardown_script setupParams: " + str(setupParams))
    servicetype = setupParams.get('servicetype')
    if servicetype == "L2DOMAIN-IRB":
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
               interface "irbvpls-%(vplsSvc_id)s"
                  no vpls
                  vrrp %(vrrp_ID)s shut
                  no vrrp %(vrrp_ID)s
                  shutdown
                  exit
               no interface "irbvpls-%(vplsSvc_id)s"
               shutdown
            exit
        no vprn %(vprnSvc_id)s
        exit

      """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vprnSvc_id': setupParams['vprnSvc_id'], 'vni': setupParams['vni'], 'vrrp_ID': setupParams['vrrp_ID']})
        return setupParams


d = {"script": (setup_script, None, None, teardown_script)}

dyn.action(d)
