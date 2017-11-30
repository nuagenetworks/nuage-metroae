This role includes common repetitive tasks for all roles inr MetroAG.

- host_reachebility_test:
  This tasks doing the following:
    - check if `hostname` variable is defined
    - go to each DNS server defined by `dns_server_list` in `build_vars.yml` and resolve `hostname` 
    - check DNS servers response. Role will fail if responses are inconsistent or IP address provided by DNS server does not match `expected_resolved_ip`
    - check that there is no SSH server run on `hostname`

  How to use:
  include the following block before start `predeployment` role
    ```yml
    - name: Check if hostname can be resolved and IP is not used
      include_role:
        name: common
        tasks_from: host_reachability_test.yml
      vars:
        expected_resolved_ip: "{{ mgmt_ip }}"
    ```
