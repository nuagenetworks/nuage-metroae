# Deploy VSD cluster with interface disabled

You can use this procedure to deploy new VSD vm with interfaces `disabled` on vcenter. You can then follow the normal uprade procedure which enables interfaces on the deployed vsd cluster vm. Using `vcenter_start_vsd_with_interfaces_disabled` flag, you can spin up new vm which have disabled interfaces. Later stage during the upgrade the interfaces enabled by `vcenter-enable-interface.yml` playbook.

When you use MetroAE to predeploy vsd vm, the common.yml in your deployment must set the `vcenter_start_vsd_with_interfaces_disabled` variable to `true`. 

When your deployment is correct, use the normal upgrade command to upgrade the vsd cluster which will deploy the new vm with disabled inteface and during the upgrade procedure it will enables the interface itself.

```
metroae upgrade vsds [deployment_name]
````

Also this can also be done during full upgrade i.e. all component upgrade including vsds, vscs, vcins, nuhs for that similar deployment needs to set. After that following command will upgrade nuage components.

```
metroae upgrade everything [deployment_name]
```