from library.vsd_monit import main
from mock import patch, MagicMock

MODULE_PATCH = "library.vsd_monit.AnsibleModule"
TEST_PARAMS = {
    "group": "all"
}

MONIT_OUTPUT = """
The Monit daemon 5.17.1 uptime: 4m

Program 'ejabberd-status'           Status ok
Program 'ejabberd'                  Status ok
Process 'vsd-stats'                 Running
"""


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


def setup_monit(mock_module):
    mock_module.get_bin_path.return_value = "/usr/bin/monit"
    mock_module.run_command.return_value = (0, MONIT_OUTPUT, "")


def verify_monit(mock_module, group):
    mock_module.get_bin_path.assert_called_once_with("monit", True)
    if group == "all":
        mock_module.run_command.assert_called_once_with(
            "/usr/bin/monit summary", check_rc=True)
    else:
        mock_module.run_command.assert_called_once_with(
            "/usr/bin/monit summary -g " + group, check_rc=True)


@patch(MODULE_PATCH)
def test_all__success(module_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module)

    main()

    verify_monit(mock_module, "all")
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(
        changed=True,
        state={"ejabberd-status": "status ok",
               "ejabberd": "status ok",
               "vsd-stats": "running"})


@patch(MODULE_PATCH)
def test_group__success(module_patch):
    params = dict(TEST_PARAMS)
    params['group'] = "vsd-stats"
    mock_module = setup_module(module_patch, params)
    setup_monit(mock_module)

    main()

    verify_monit(mock_module, "vsd-stats")
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(
        changed=True,
        state={"ejabberd-status": "status ok",
               "ejabberd": "status ok",
               "vsd-stats": "running"})


@patch(MODULE_PATCH)
def test_all__monit_error(module_patch):
    mock_module = setup_module(module_patch)
    setup_monit(mock_module)
    mock_module.run_command.return_value = (255, "stdout", "stderr")

    main()

    verify_monit(mock_module, "all")
    mock_module.fail_json.assert_called_once_with(msg="command failed",
                                                  rc=255,
                                                  cmd="/usr/bin/monit summary",
                                                  stdout="stdout",
                                                  stderr="stderr",
                                                  changed=False)
