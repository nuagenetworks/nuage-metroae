from library.monit_waitfor_service import main
from mock import call, patch, MagicMock

MODULE_PATCH = "library.monit_waitfor_service.AnsibleModule"
TEST_PARAMS = {
    "name": ["ejabberd-status"],
    "timeout_seconds": 90,
    "test_interval_seconds": 30
}

MONIT_OUTPUT = """
The Monit daemon 5.17.1 uptime: 4m

Program 'ejabberd-status'           %s
"""


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


def setup_monit(mock_module, output):
    mock_module.get_bin_path.return_value = "/usr/bin/monit"
    mock_module.run_command.return_value = (0, output, "")


def verify_monit(mock_module, num_calls):
    mock_module.get_bin_path.assert_called_once_with("monit", True)
    calls = list()
    for i in range(num_calls):
        calls.append(call("/usr/bin/monit summary " + TEST_PARAMS["name"][0],
                          check_rc=True))
    mock_module.run_command.assert_has_calls(calls)
    assert mock_module.run_command.call_count == num_calls


def create_expected_state(state, num_calls):
    return {
        TEST_PARAMS["name"][0]: state.lower(),
        "Desired state": True,
        "Time taken": (num_calls - 1) * TEST_PARAMS["test_interval_seconds"]
    }


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__status_ok(module_patch, sleep_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module, MONIT_OUTPUT % "Status ok")
    sleep_patch.return_value = None

    main()

    sleep_patch.assert_not_called()
    verify_monit(mock_module, 1)
    state = create_expected_state("Status ok", 1)
    mock_module.exit_json.assert_called_once_with(changed=True,
                                                  name=TEST_PARAMS["name"][0],
                                                  state=state)


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__stopped(module_patch, sleep_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module, MONIT_OUTPUT % "Stopped")
    sleep_patch.return_value = None

    main()

    assert sleep_patch.call_count == 3
    verify_monit(mock_module, 4)
    mock_module.fail_json.assert_called_once_with(
        msg="Process %s did not transition to active within %i seconds" % (
            TEST_PARAMS["name"][0], TEST_PARAMS["timeout_seconds"]))


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__waiting(module_patch, sleep_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module, MONIT_OUTPUT % "Waiting")
    mock_module.run_command.side_effect = [
        (0, MONIT_OUTPUT % "Waiting", ""),
        (0, MONIT_OUTPUT % "Waiting", ""),
        (0, MONIT_OUTPUT % "Running", "")]
    sleep_patch.return_value = None

    main()

    assert sleep_patch.call_count == 2
    verify_monit(mock_module, 3)
    state = create_expected_state("Running", 3)
    mock_module.exit_json.assert_called_once_with(changed=True,
                                                  name=TEST_PARAMS["name"][0],
                                                  state=state)


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__wrong_process(module_patch, sleep_patch):
    params = dict(TEST_PARAMS)
    params["name"] = ["foobar"]
    mock_module = setup_module(module_patch, params)
    setup_monit(mock_module, MONIT_OUTPUT % "Stopped")
    sleep_patch.return_value = None

    main()

    assert sleep_patch.call_count == 3
    assert mock_module.run_command.call_count == 4
    mock_module.fail_json.assert_called_once_with(
        msg="Process %s did not transition to active within %i seconds" % (
            "foobar", TEST_PARAMS["timeout_seconds"]))


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__restart_success(module_patch, sleep_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module, MONIT_OUTPUT % "Failed")
    mock_module.run_command.side_effect = [
        (0, MONIT_OUTPUT % "Failed", ""),
        (0, MONIT_OUTPUT % "Failed", ""),
        (0, MONIT_OUTPUT % "Failed", ""),
        (0, MONIT_OUTPUT % "Running", "")]
    sleep_patch.return_value = None

    main()

    assert sleep_patch.call_count == 2
    assert mock_module.run_command.call_count == 4
    mock_module.run_command.assert_has_calls(
        [call("/usr/bin/monit restart " + TEST_PARAMS["name"][0],
              check_rc=True)])
    state = create_expected_state("Running", 3)
    mock_module.exit_json.assert_called_once_with(changed=True,
                                                  name=TEST_PARAMS["name"][0],
                                                  state=state)


@patch("time.sleep")
@patch(MODULE_PATCH)
def test__restart_failed(module_patch, sleep_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module, MONIT_OUTPUT % "Failed")
    sleep_patch.return_value = None

    main()

    assert sleep_patch.call_count == 3
    assert mock_module.run_command.call_count == 5
    mock_module.run_command.assert_has_calls(
        [call("/usr/bin/monit restart " + TEST_PARAMS["name"][0],
              check_rc=True)])
    mock_module.fail_json.assert_called_once_with(
        msg="Process %s did not transition to active within %i seconds" % (
            TEST_PARAMS["name"][0], TEST_PARAMS["timeout_seconds"]))
