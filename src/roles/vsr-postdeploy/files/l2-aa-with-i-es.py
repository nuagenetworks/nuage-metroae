from alc import dyn
# note 1: an I-ES must be manually configured upfront (under 'configure service system bgp-evpn ethernet-segment ...' - see I-ES ACG). This only need to be done once and then I-ES can be re-used for multiple fully-dynamiced created services.
# note 2: the script offsets the dyn.select_free_id function with 500 to avoid issues with other L2VXLAN-IRB/L3VXLAN services. Hence the configured I-ES service range starting point should be 500 higher than the vsd service range start point. Eg vsd service range 64000-64999 and I-ES service range 64500-64999.
# note 3: this script can be used for a redundant DC-GW pair. Make sure you a different RD on each DC-GW
# note 4: in case you use redundant DC-GWs you also need to provide
# routing policies (manually at bgp level) to avoid routing loops. See
# also ACG.

# example of metadata to be added in VSD WAN Service:
# "rddc=1:30000,rdwan=10.0.0.1:3000,rtwan=65000:3000"

# example of tools cli to test this script: tools perform service vsd evaluate-script domain-name "l2dom1" type l2-domain action setup policy "py-l2-I-ES" vni 1234 rt-i target:1:1 rt-e target:1:1 metadata "rddc=1:30000,rdwan=10.0.0.1:3000,rtwan=65000:3000"
# teardown example cli: tools perform service vsd evaluate-script
# domain-name "l2dom1" type l2-domain action teardown policy "py-l2-I-ES"
# vni 1234 rt-i target:1:1 rt-e target:1:1


def setup_script(vsdParams):

    print("These are the VSD params: " + str(vsdParams))
    servicetype = vsdParams['servicetype']
    vni = vsdParams['vni']
    rtdc = vsdParams['rt']

# add "target:" if provisioned by VSD (VSD uses x:x format whereas tools
# command uses target:x:x format)
    if not rtdc.startswith('target'):
        rtdc = "target:" + rtdc

    metadata = vsdParams['metadata']

# remove trailing space at the end of the metadata
    metadata = metadata.rstrip()

    print("VSD metadata" + str(metadata))

    metadata = dict(e.split('=') for e in metadata.split(','))
    print("Modified metadata" + str(metadata))
    vplsSvc_id = str(int(dyn.select_free_id("service-id")) + 500)
    print("this is the free svc id picked up by the system: " + vplsSvc_id)

    if servicetype == "L2DOMAIN":

        rddc = metadata['rddc']
        rdwan = metadata['rdwan']
        rtwan = metadata['rtwan']
        if not rtwan.startswith('target'):
            rtwan = "target:" + rtwan
        print('servicetype, VPLS id, rtdc, vni, rddc, rdwan, rtwan:',
               servicetype, vplsSvc_id, rtdc, vni, rddc, rdwan, rtwan)
        dyn.add_cli("""
        configure service
           vpls %(vplsSvc_id)s customer 1 create
              description vpls%(vplsSvc_id)s
              bgp
                 route-distinguisher %(rddc)s
                 route-target %(rtdc)s
              exit
              bgp 2
                 route-distinguisher %(rdwan)s
                 route-target %(rtwan)s
              exit
              vxlan vni %(vni)s create
              exit
              bgp-evpn
                  evi %(vplsSvc_id)s
                  vxlan
                      no shut
                  exit
                  mpls
                      ingress-replication-bum-label
                      ecmp 2
                      bgp-instance 2
                      auto-bind-tunnel
                          resolution any
                      exit
                      no shutdown
                  exit
              exit
              no shutdown
              exit
            exit
        exit
      """ % {'vplsSvc_id': vplsSvc_id, 'vni': vsdParams['vni'], 'rtdc': rtdc, 'rddc': rddc, 'rdwan': rdwan, 'rtwan': rtwan})
        # L2DOMAIN returns setupParams: vplsSvc_id, servicetype, vni
        return {'vplsSvc_id': vplsSvc_id,
                'servicetype': servicetype, 'vni': vni}

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
               bgp-evpn
                   vxlan
                       shut
                   exit
                   mpls
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
               bgp 2
                  no route-distinguisher
                  no route-target
               exit
               no bgp 2
               no bgp-evpn
               shutdown
               exit
               no vpls %(vplsSvc_id)s
            exit
        exit
      """ % {'vplsSvc_id': setupParams['vplsSvc_id'], 'vni': setupParams['vni']})
        return setupParams


d = {"script": (setup_script, modify_script, revert_script, teardown_script)}

dyn.action(d)
