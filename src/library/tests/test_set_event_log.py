from library.set_event_log import main
from mock import patch, MagicMock

MODULE_PATCH = "library.set_event_log.AnsibleModule"
YAML_PATCH = "library.set_event_log.AnsibleModule"
TEST_PARAMS = {
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443"},
    "api_version": "5.2.3",
    "event_log_age": "7"
}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


class TestSetEventLog(object):

    def setup_session_root(self, import_patch):
        self.mock_vspk = MagicMock()
        import_patch.return_value = self.mock_vspk

        self.mock_session = MagicMock()
        mock_root = MagicMock()
        self.mock_session.user = mock_root
        self.mock_vspk.NUVSDSession.return_value = self.mock_session

        return mock_root

    def setup_system_configs(self, mock_root):
        mock_sys_config = MagicMock()
        mock_root.system_configs.get_first.return_value = mock_sys_config

        return mock_sys_config

    def validate_standard(self, import_patch):
        import_patch.assert_called_once_with("vspk.v5_0")
        self.mock_vspk.NUVSDSession.assert_called_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_with()

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__success(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        mock_sys_config = self.setup_system_configs(mock_root)

        main()

        self.validate_standard(import_patch)
        assert mock_sys_config.event_log_entry_max_age == TEST_PARAMS[
            "event_log_age"]
        mock_sys_config.save.assert_called_once_with()
        mock_module.exit_json.assert_called_once_with(
            changed=True,
            result="Event log age set to %s" % TEST_PARAMS["event_log_age"])

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_import(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        import_patch.side_effect = ImportError("cannot import")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg='vspk is required for this module, or '
            'API version specified does not exist.')
