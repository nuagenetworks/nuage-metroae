from bambou import exceptions
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

    def setup_sys_config(self, mock_root):
        mock_sys_config = MagicMock()

        mock_root.system_configs = MagicMock()
        mock_root.system_configs.get_first.return_value = mock_sys_config

        return mock_sys_config

    def get_mock_bambou_error(self, status_code, reason):
        return exceptions.BambouHTTPError(
            type('', (object,), {
                'response': type('', (object,), {'status_code': status_code,
                                                 'reason': reason,
                                                 'errors': reason})()})())

    def validate_standard(self, import_patch):
        import_patch.assert_called_once_with("vspk.v5_0")
        self.mock_vspk.NUVSDSession.assert_called_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_with()

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_get__success(self, module_patch, import_patch):
        params = dict(TEST_PARAMS)
        params['get_gateway_purge_time'] = True
        mock_module = self.setup_module(module_patch, params)
        mock_root = self.setup_session_root(import_patch)

        mock_sys_config = self.setup_sys_config(mock_root)
        mock_sys_config.ad_gateway_purge_time = 12345

        main()

        self.validate_standard(import_patch)
        mock_module.exit_json.assert_called_once_with(changed=True,
                                                      result=12345)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_get__exception(self, module_patch, import_patch):
        params = dict(TEST_PARAMS)
        params['get_gateway_purge_time'] = True
        mock_module = self.setup_module(module_patch, params)
        mock_root = self.setup_session_root(import_patch)

        mock_root.system_configs = MagicMock()
        mock_root.system_configs.get_first.side_effect = Exception("Test")

        main()

        self.validate_standard(import_patch)
        mock_module.fail_json.assert_called_once_with(
            msg="Could not retrieve gateway purge timer : Test")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_set__success(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)

        mock_sys_config = self.setup_sys_config(mock_root)

        main()

        gw_purge = TEST_PARAMS['gateway_purge_time']

        self.validate_standard(import_patch)
        assert mock_sys_config.ad_gateway_purge_time == gw_purge
        mock_sys_config.save.assert_called_once_with()
        mock_module.exit_json.assert_called_once_with(
            changed=True,
            result="Gateway purge time set to %ssec" % gw_purge)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_set__already_set(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)

        mock_sys_config = self.setup_sys_config(mock_root)
        mock_sys_config.save.side_effect = self.get_mock_bambou_error(
            400, "There are no attribute changes")

        main()

        gw_purge = TEST_PARAMS['gateway_purge_time']

        self.validate_standard(import_patch)
        assert mock_sys_config.ad_gateway_purge_time == gw_purge
        mock_sys_config.save.assert_called_once_with()
        mock_module.exit_json.assert_called_once_with(
            changed=True,
            result="Gateway time is already updated to %s" % gw_purge)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_set__update_error(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)

        mock_sys_config = self.setup_sys_config(mock_root)
        mock_sys_config.save.side_effect = Exception("Test")

        main()

        gw_purge = TEST_PARAMS['gateway_purge_time']

        self.validate_standard(import_patch)
        assert mock_sys_config.ad_gateway_purge_time == gw_purge
        mock_sys_config.save.assert_called_once_with()
        mock_module.fail_json.assert_called_once_with(
            msg="Could not update gateway purge timer : Test")

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

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_connect(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        self.setup_session_root(import_patch)

        self.mock_session.start.side_effect = Exception("cannot connect")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="Could not establish connection to VSD cannot connect")
