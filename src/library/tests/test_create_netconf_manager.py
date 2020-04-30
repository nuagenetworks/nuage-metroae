from library.create_netconf_manager import main
from mock import call, patch, MagicMock

MODULE_PATCH = "library.create_netconf_manager.AnsibleModule"
YAML_PATCH = "library.create_netconf_manager.AnsibleModule"
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

    def setup_session(self, import_patch):
        self.mock_vspk = MagicMock()
        import_patch.return_value = self.mock_vspk
        self.mock_session = MagicMock()
        mock_root = MagicMock()
        self.mock_session.user = mock_root
        self.mock_vspk.NUVSDSession.return_value = self.mock_session

        return mock_root

    def make_mock_ent(self, name, ent_id):
        ent = MagicMock()
        ent.name = name
        ent.id = ent_id
        return ent

    def setup_enterprise(self, mock_root):
        self.enterprises = [
            self.make_mock_ent("Shared Infrastructure", 1),
            self.make_mock_ent("ent2", 2),
            self.make_mock_ent("ent3", 3)
        ]
        mock_root.enterprises.get.return_value = self.enterprises

    def verify_session(self, import_patch):
        import_patch.assert_called_once_with("vspk.v5_0")
        self.mock_vspk.NUVSDSession.assert_called_once_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_once_with()

    def verify_netconf_user(self, import_patch):
        import_patch.NUUser.assert_has_calls([call(
            first_name=TEST_PARAMS["netconf_manager_user"]['firstName'],
            last_name=TEST_PARAMS["netconf_manager_user"]['lastName'],
            user_name=TEST_PARAMS["netconf_manager_user"]['netconf_user'],
            email=TEST_PARAMS["netconf_manager_user"]['email'],
            password=TEST_PARAMS["netconf_manager_user"]['password'])])

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_iso_create__success(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session(import_patch)
        self.setup_enterprise(mock_root)

        main()

        self.verify_session(import_patch)
        self.verify_netconf_user(import_patch)

        mock_module.fail_json.assert_not_called()

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_connect(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        self.setup_session(import_patch)
        self.mock_session.start.side_effect = Exception("cannot connect")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="Could not establish connection to VSD cannot connect")
