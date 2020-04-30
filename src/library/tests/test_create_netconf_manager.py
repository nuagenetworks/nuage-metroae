from library.create_netconf_manager import main
from mock import call, patch, MagicMock

MODULE_PATCH = "library.create_netconf_manager.AnsibleModule"
VSPK_PATCH = "library.create_netconf_manager.VSPK"
TEST_PARAMS = {
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443"},
    "netconf_manager_user": {
        "firstName": "John",
        "lastName": "Doe",
        "email": "user@email.com",
        "password": "pass",
        "netconf_user": "proxy"},
    "vsd_version": "5.4.1"
}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


class TestCreateNetconfManager(object):

    def setup_session(self, vspk_patch):
        self.mock_vspk = MagicMock()
        vspk_patch.return_value = self.mock_vspk
        self.mock_session = MagicMock()

        self.mock_root = MagicMock()
        self.mock_session.user = self.mock_root
        self.mock_vspk.NUVSDSession.return_value = self.mock_session

    def verify_session(self, vspk_patch):
        self.mock_vspk.NUVSDSession.assert_called_once_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_once_with()

    def verify_netconf_user(self, vspk_patch):
        vspk_patch.NUUser.assert_has_calls([call(
            first_name=TEST_PARAMS["netconf_manager_user"]['firstName'],
            last_name=TEST_PARAMS["netconf_manager_user"]['lastName'],
            user_name=TEST_PARAMS["netconf_manager_user"]['netconf_user'],
            email=TEST_PARAMS["netconf_manager_user"]['email'],
            password=TEST_PARAMS["netconf_manager_user"]['password'])])

    @patch(MODULE_PATCH)
    @patch(VSPK_PATCH)
    @patch("subprocess.call")
    def test_iso_create__success(self, mock_subproc, vspk_patch, module_patch):
        mock_module = setup_module(module_patch)
        self.setup_session(vspk_patch)

        main()

        self.verify_session(vspk_patch)
        self.verify_netconf_user(vspk_patch)

        mock_module.fail_json.assert_not_called()

    @patch(MODULE_PATCH)
    @patch(VSPK_PATCH)
    def test__cannot_connect(self, vspk_patch, module_patch):
        mock_module = setup_module(module_patch)

        mock_session = MagicMock()
        self.mock_vspk.NUVSDSession.return_value = mock_session
        mock_session.start.side_effect = Exception("Test")

        main()

        mock_module.fail_json.assert_called_once()
        args, kwargs = mock_module.fail_json.call_args_list[0]
        assert "ERROR: Could not establish connection to VSD" in kwargs["msg"]
