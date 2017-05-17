# Deploy STCv VM on KVM hosts

STCv vm deployment is supported via the stcv-vm-predeploy and stc-vm-postdeploy roles.

To run STCv vm deployment:

1. Edit `stcv_build_vars.yml` to customize your deployment.
1. Execute `ansible-playbook stcv_vm_predeploy.yml`
1. Wait sufficient time for STCV to boot...
1. Execute `ansible-playbook stcv_vm_postdeploy.yml`
