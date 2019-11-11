from library.config_vsd_system import main
from mock import patch, MagicMock

MODULE_PATCH = "library.config_vsd_system.AnsibleModule"
TEST_PARAMS = {
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443"},
    "gateway_purge_time": 7003,
    "get_gateway_purge_time": False
}


class TestConfigVsdSystem(object):

    def setup_module(self, module_patch, params=None):
        mock_module = MagicMock()
        module_patch.return_value = mock_module
        if params is None:
            mock_module.params = TEST_PARAMS
        else:
            mock_module.params = params

        return mock_module

    def setup_session_root(self, import_patch):
        self.mock_vspk = MagicMock()
        import_patch.return_value = self.mock_vspk

        self.mock_session = MagicMock()
        mock_root = MagicMock()
        self.mock_session.user = mock_root
        self.mock_vspk.NUVSDSession.return_value = self.mock_session

        return mock_root

    def validate_standard(self, import_patch):
        import_patch.assert_called_once_with("vspk.v5_0")
        self.mock_vspk.NUVSDSession.assert_called_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_with()

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_get__success(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)

        main()

        self.validate_standard(import_patch)
        mock_module.exit_json.assert_called_once_with(changed=False,
                                                      result="True")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_import(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)

        import_patch.side_effect = ImportError("cannot import")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="vspk is required for this module, or "
            "API version specified does not exist.")
