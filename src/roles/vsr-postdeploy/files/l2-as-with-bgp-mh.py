from alc import dyn

# example of metadata to be added in VSD WAN Service:
# "rd=1:1,sap=1/1/3:1000,opergroup=group-PE1"

# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l2dom1" type l2-domain action setup policy "py-l2-red" vni 1234 rt-i target:1:1 rt-e target:1:1 metadata "rd=1:1,sap=1/1/3:1000,opergroup=group-PE1"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l2dom1" type l2-domain action teardown policy "py-l2-red"
# vni 1234 rt-i target:1:1 rt-e target:1:1


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
    print("this is the free svc id picked up by the system: " + vplsSvc_id)

    if servicetype == "L2DOMAIN":

        rd = metadata['rd']
        sap = metadata['sap']
        opergroup = metadata['opergroup']
        print('servicetype, VPLS id, rt, vni, rd, sap, opergroup:',
              servicetype, vplsSvc_id, rt, vni, rd, sap, opergroup)
        dyn.add_cli("""
        configure service
           vpls %(vplsSvc_id)s customer 1 name  evi%(vplsSvc_id)s create
              description vpls%(vplsSvc_id)s
              proxy-arp
                 dynamic-arp-populate
                 no shut
                 exit
              bgp
                 route-distinguisher %(rd)s
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
              sap %(sap)s create
                  monitor-oper-group %(opergroup)s
                  no shutdown
              exit
              no shutdown
              exit
            exit
        exit
      """ % {'vplsSvc_id': vplsSvc_id, 'vni': vsdParams['vni'], 'rt': rt, 'rd': metadata['rd'], 'sap': sap, 'opergroup': metadata['opergroup']})
        # L2DOMAIN returns setupParams: vplsSvc_id, servicetype, vni, sdp,
        # opergroup
        return {'vplsSvc_id': vplsSvc_id, 'servicetype': servicetype,
                'vni': vni, 'sap': sap, 'opergroup': opergroup}

# ------------------------------------------------------------------------------------------------


def modify_script(vsdParams, setup_result):

    print(
        "These are the setup_result params for modify_script: " +
        str(setup_result))
    print("These are the VSD params for modify_script: " + str(vsdParams))

    # remove trailing space at the end of the metadata
    metadata = vsdParams['metadata'].rstrip()

    print("VSD metadata" + str(metadata))
    metadata = dict(e.split('=') for e in metadata.split(','))
    print("Modified metadata" + str(metadata))

    # updating the setup_result dict
    setup_result.update(metadata)
    params = setup_result

    print(
        "The updated params from metadata and return from the setup result: " +
        str(params))

    dyn.add_cli("""
      configure service
          vpls %(vplsSvc_id)s
            service-mtu %(svc-mtu)s
             exit
          exit
      exit
    """ % params)

    # Result is passed to teardown_script
    return params

# ------------------------------------------------------------------------------------------------


def revert_script(vsdParams, setup_result):
    print(
        "These are the setup_result params for revert_script: " +
        str(setup_result))
    print("These are the VSD params for revert_script: " + str(vsdParams))

    # When modify fails, the revert is called and then the teardown is called.
    # It is recommended to revert to same value as used in setup for the
    # attributes modified in modify_script.

    params = setup_result

    dyn.add_cli("""
      configure service
          vpls %(vplsSvc_id)s
            service-mtu 2000
             exit
          exit
      exit
    """ % params)

    # Result is passed to teardown_script
    return params

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
               no bgp
               no bgp-evpn
               sap %(sap)s
                  shutdown
                  exit
               no sap %(sap)s
               shutdown
               exit
               no vpls %(vplsSvc_id)s
            exit
        exit
      """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vni': setupParams['vni'], 'sap': setupParams['sap']})
        return setupParams


d = {"script": (setup_script, modify_script, revert_script, teardown_script)}

dyn.action(d)
