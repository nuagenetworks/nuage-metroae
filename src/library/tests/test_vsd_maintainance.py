from bambou import exceptions
from library.vsd_maintainance import main
from mock import patch, MagicMock

MODULE_PATCH = "library.vsd_maintainance.AnsibleModule"
YAML_PATCH = "library.vsd_maintainance.AnsibleModule"
TEST_PARAMS = {
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443"},
    "state": "enabled"
}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


class TestVsdMaintainance(object):

    def setup_session_root(self, import_patch):
        self.mock_vspk = MagicMock()
        import_patch.return_value = self.mock_vspk

        self.mock_session = MagicMock()
        mock_root = MagicMock()
        self.mock_session.user = mock_root
        self.mock_vspk.NUVSDSession.return_value = self.mock_session

        return mock_root

    def validate_session(self, import_patch):
        import_patch.assert_called_once_with("vspk.v5_0")
        self.mock_vspk.NUVSDSession.assert_called_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_with()

    def make_mock_ent(self, name, ent_id):
        ent = MagicMock()
        ent.name = name
        ent.id = ent_id
        return ent

    def make_mock_domain(self, ent_id, error_msg=None):
        domain = MagicMock()
        domain.maintenance_mode = "UNSET"
        domain.parent_id = ent_id
        if error_msg is not None:
            domain.save.side_effect = Exception(error_msg)
        return domain

    def setup_sample_domains(self, mock_root):
        self.enterprises = [
            self.make_mock_ent("Shared Infrastructure", 1),
            self.make_mock_ent("ent2", 2),
            self.make_mock_ent("ent3", 3)
        ]
        mock_root.enterprises.get.return_value = self.enterprises

        self.l3_domains = [
            self.make_mock_domain(1, "Should not set"),
            self.make_mock_domain(2),
            self.make_mock_domain(3),
            self.make_mock_domain(4)
        ]

        mock_root.domains.get.return_value = self.l3_domains

        self.l2_domains = [
            self.make_mock_domain(1, "Should not set"),
            self.make_mock_domain(2),
            self.make_mock_domain(3),
            self.make_mock_domain(4)
        ]

        mock_root.l2_domains.get.return_value = self.l2_domains

    def validate_sample_domains(self, mock_root, state):
        mock_root.enterprises.get.assert_called_once_with()
        mock_root.domains.get.assert_called_once_with()
        mock_root.l2_domains.get.assert_called_once_with()

        assert self.l3_domains[0].maintenance_mode == "UNSET"
        assert self.l3_domains[1].maintenance_mode == state
        assert self.l3_domains[2].maintenance_mode == state
        assert self.l3_domains[3].maintenance_mode == "UNSET"

        self.l3_domains[0].save.assert_not_called()
        self.l3_domains[1].save.assert_called_once_with()
        self.l3_domains[2].save.assert_called_once_with()
        self.l3_domains[3].save.assert_not_called()

        assert self.l2_domains[0].maintenance_mode == "UNSET"
        assert self.l2_domains[1].maintenance_mode == state
        assert self.l2_domains[2].maintenance_mode == state
        assert self.l2_domains[3].maintenance_mode == "UNSET"

        self.l2_domains[0].save.assert_not_called()
        self.l2_domains[1].save.assert_called_once_with()
        self.l2_domains[2].save.assert_called_once_with()
        self.l2_domains[3].save.assert_not_called()

    def get_mock_bambou_error(self, status_code, reason):
        return exceptions.BambouHTTPError(
            type('', (object,), {
                'response': type('', (object,), {'status_code': status_code,
                                                 'reason': reason,
                                                 'errors': reason})()})())

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_enable__success(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)

        main()

        self.validate_session(import_patch)
        self.validate_sample_domains(mock_root, "ENABLED")

        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            rc=0, changed=True,
            result="Maintainance mode for all non shared L3 domains-enabled, "
            "Maintainance mode for all non shared L2 domains-enabled,")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_disable__success(self, module_patch, import_patch):
        params = dict(TEST_PARAMS)
        params["state"] = "disabled"
        mock_module = setup_module(module_patch, params)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)

        main()

        self.validate_session(import_patch)
        self.validate_sample_domains(mock_root, "DISABLED")

        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            rc=0, changed=True,
            result="Maintainance mode for all non shared L3 domains-disabled, "
            "Maintainance mode for all non shared L2 domains-disabled,")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_enable__no_domains(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)
        mock_root.domains.get.return_value = list()
        mock_root.l2_domains.get.return_value = list()

        main()

        self.validate_session(import_patch)

        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            rc=0, changed=True,
            result="No L3 domains found to enabled maintainance mode, "
            "No L2 domains found to enabled maintainance mode")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test_reserved__success(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)
        self.l3_domains[1].save.side_effect = Exception("Domain is reserved")

        main()

        self.validate_session(import_patch)
        self.validate_sample_domains(mock_root, "ENABLED")

        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            rc=0, changed=True,
            result="Maintainance mode for all non shared L3 domains-enabled, "
            "Maintainance mode for all non shared L2 domains-enabled,")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_import(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        import_patch.side_effect = ImportError("cannot import")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg='vspk is required for this module, or '
            'API version specified does not exist.', rc=1)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_connect(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        self.setup_session_root(import_patch)
        self.mock_session.start.side_effect = Exception("cannot connect")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="Could not establish connection to VSD cannot connect", rc=1)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__no_changes(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)
        self.l3_domains[1].save.side_effect = self.get_mock_bambou_error(
            400, "There are no attribute changes")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            rc=0, changed=True,
            result="Maintainance mode is already enabled")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__bambou_error(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)
        self.l3_domains[1].save.side_effect = self.get_mock_bambou_error(
            400, "save error")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="Could not set maintainance mode : "
            "[HTTP 400(save error)] save error", rc=1)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__exception(self, module_patch, import_patch):
        mock_module = setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        self.setup_sample_domains(mock_root)
        self.l3_domains[1].save.side_effect = Exception("cannot save")

        main()

        import_patch.assert_called_once_with("vspk.v5_0")
        mock_module.fail_json.assert_called_once_with(
            msg="Could not set maintainance mode : cannot save", rc=1)
