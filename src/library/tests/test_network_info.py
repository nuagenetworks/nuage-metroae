from library.network_info import main
from mock import call, patch, MagicMock

MODULE_PATCH = "library.network_info.AnsibleModule"
TEST_PARAMS = {
    "mac_addr": True,
}

IP_OUTPUT = """
1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever preferred_lft forever
15: docker0    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0\\       valid_lft forever preferred_lft forever
17: bridge0    inet 135.227.221.68/24 brd 135.227.221.255 scope global bridge0\\       valid_lft forever preferred_lft forever
17: bridge0    inet 10.32.8.11/20 brd 10.32.15.255 scope global bridge0:1\\       valid_lft forever preferred_lft forever
"""

MAC_OUTPUT = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1\\    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eno1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000\\    link/ether 0c:c4:7a:a9:4e:b4 brd ff:ff:ff:ff:ff:ff
3: eno2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000\\    link/ether 0c:c4:7a:a9:4e:b5 brd ff:ff:ff:ff:ff:ff
4: eno3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000\\    link/ether 0c:c4:7a:a9:4e:b6 brd ff:ff:ff:ff:ff:ff
5: eno4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master bridge0 state UP group default qlen 1000\\    link/ether 0c:c4:7a:a9:4e:b7 brd ff:ff:ff:ff:ff:ff
15: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default \\    link/ether 02:42:86:a0:94:a0 brd ff:ff:ff:ff:ff:ff
17: bridge0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000\\    link/ether 0c:c4:7a:a9:4e:b7 brd ff:ff:ff:ff:ff:ff
"""


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


def setup_run_command(mock_module, output_list):
    mock_module.get_bin_path.side_effect = ["/usr/sbin/ip",
                                            "/usr/bin/hostname"]
    outputs = [(0, output, "") for output in output_list]
    mock_module.run_command.side_effect = outputs


def validate_module(mock_module):
    mock_module.get_bin_path.assert_has_calls(
        [call('ip', True), call('hostname', True)])
    mock_module.run_command.assert_has_calls(
        [call("/usr/sbin/ip -o -family inet addr", check_rc=False),
         call("/usr/sbin/ip -o -family link addr", check_rc=False),
         call("/usr/bin/hostname -f", check_rc=False)])


@patch(MODULE_PATCH)
def test__addresses(module_patch):
    params = dict(TEST_PARAMS)
    params["mac_addr"] = False
    mock_module = setup_module(module_patch, params)

    setup_run_command(mock_module, [IP_OUTPUT, MAC_OUTPUT, "vsd1.example.met"])

    main()

    validate_module(mock_module)
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(
        changed=True,
        cmd=IP_OUTPUT,
        info={
            'interfaces': {'lo': {'ip': '127.0.0.1'},
                           'bridge0': {'ip': '10.32.8.11'},
                           'docker0': {'ip': '172.17.0.1'}},
            'hostname': 'vsd1.example.met'},
        rawout=(IP_OUTPUT, MAC_OUTPUT))


@patch(MODULE_PATCH)
def test__macs(module_patch):
    params = dict(TEST_PARAMS)
    params["mac_addr"] = True
    mock_module = setup_module(module_patch, params)

    setup_run_command(mock_module, [IP_OUTPUT, MAC_OUTPUT, "vsd1.example.met"])

    main()

    validate_module(mock_module)
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(
        changed=True,
        cmd=IP_OUTPUT,
        info={
            'interfaces': {'lo': {'ip': '127.0.0.1'},
                           'bridge0': {'ip': '10.32.8.11',
                                       'mac_addr': '0c:c4:7a:a9:4e:b7'},
                           'docker0': {'ip': '172.17.0.1',
                                       'mac_addr': '02:42:86:a0:94:a0'}},
            'hostname': 'vsd1.example.met'},
        rawout=(IP_OUTPUT, MAC_OUTPUT))


@patch(MODULE_PATCH)
def test__command_error(module_patch):
    params = dict(TEST_PARAMS)
    params["mac_addr"] = True
    mock_module = setup_module(module_patch, params)
    setup_run_command(mock_module, [IP_OUTPUT, MAC_OUTPUT, "vsd1.example.met"])
    mock_module.run_command.side_effect = [
        (255, "error message", "stderr"),
        (255, "error message", "stderr"),
        (0, "vsd1.example.met", "")]

    main()

    mock_module.fail_json.assert_has_calls(
        [call(msg="command failed",
              rc=255,
              cmd="/usr/sbin/ip -o -family inet addr",
              stdout="error message",
              stderr="stderr",
              changed=False)])
