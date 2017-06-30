# Deploy STCv VM on KVM hosts

STCv vm deployment is supported via the stcv-predeploy and stc-postdeploy roles.

To run STCv vm deployment:

1. Edit `stcv_build_vars.yml` to customize your deployment.
1. Execute `ansible-playbook stcv_predeploy.yml`
1. Wait sufficient time for STCV to boot...
1. Execute `ansible-playbook stcv_postdeploy.yml`


# Deploy STCv VM on ESXi hosts

STCv vm deployment is supported via the stcv-predeploy and stc-postdeploy roles.

To run STCv vm deployment:

1. Edit `stcv_build_vars.yml` to customize your deployment.
   target_server_type should be vcenter
   data_bridge2 is only needed if your image supports 2 data interfaces.
1. Execute `ansible-playbook stcv_predeploy.yml`
1. Wait sufficient time for STCV to boot...
1. Execute `ansible-playbook stcv_postdeploy.yml`
