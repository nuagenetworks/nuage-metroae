from library.check_vsd_license_validity import main
from mock import patch, MagicMock

MODULE_PATCH = "library.check_vsd_license_validity.AnsibleModule"
TEST_PARAMS = {
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443",
        "api_version": "v6"},
    "required_days_left": 365
}
SECONDS_PER_DAY = 60 * 60 * 24


class TestVsdLicenseValid(object):

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

    def setup_licenses(self, mock_root, licenses):
        mock_root.licenses = MagicMock()
        mock_root.licenses.get.return_value = licenses

    def get_mock_license(self, expiry_timestamp, supported_versions, id):
        mock_license = MagicMock()
        mock_license.expiry_timestamp = expiry_timestamp * 1000
        mock_license.additional_supported_versions = supported_versions
        mock_license.unique_license_identifier = id
        mock_license.licensed_feature = "vss"
        return mock_license

    def validate_session(self, import_patch):
        import_patch.assert_called_once_with("vspk.{0:s}".format(TEST_PARAMS["vsd_auth"]["api_version"]))
        self.mock_vspk.NUVSDSession.assert_called_with(
            username=TEST_PARAMS["vsd_auth"]["username"],
            password=TEST_PARAMS["vsd_auth"]["password"],
            enterprise=TEST_PARAMS["vsd_auth"]["enterprise"],
            api_url=TEST_PARAMS["vsd_auth"]["api_url"])
        self.mock_session.start.assert_called_with()

    @patch("importlib.import_module")
    @patch("time.time")
    @patch(MODULE_PATCH)
    def test__success(self, module_patch, time_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        lic_1 = self.get_mock_license(SECONDS_PER_DAY * 366, 1, "lic1")
        lic_2 = self.get_mock_license(SECONDS_PER_DAY * 500, 1, "lic2")

        self.setup_licenses(mock_root, [lic_1, lic_2])

        time_patch.return_value = SECONDS_PER_DAY
        main()

        test_days_left_dict = {lic_1.unique_license_identifier: [365, lic_1.licensed_feature], lic_2.unique_license_identifier: [499, lic_2.licensed_feature]}
        test_valid_dict = {lic_1.unique_license_identifier: True, lic_2.unique_license_identifier: True}

        test_result_dict = {"validity": test_valid_dict, "days_left": test_days_left_dict}

        self.validate_session(import_patch)
        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(changed=False,
                                                      result=test_result_dict)

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_import(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)

        import_patch.side_effect = ImportError("cannot import")

        main()

        import_patch.assert_called_once_with("vspk.v6")
        mock_module.fail_json.assert_called_once_with(
            msg="vspk is required for this module, or "
            "API version specified does not exist.")

    @patch("importlib.import_module")
    @patch(MODULE_PATCH)
    def test__cannot_connect(self, module_patch, import_patch):
        mock_module = self.setup_module(module_patch)

        mock_vspk = MagicMock()
        import_patch.return_value = mock_vspk

        mock_session = MagicMock()
        mock_root = MagicMock()
        mock_session.user = mock_root
        mock_vspk.NUVSDSession.return_value = mock_session
        mock_session.start.side_effect = Exception("cannot connect")

        main()

        import_patch.assert_called_once_with("vspk.{0:s}".format(TEST_PARAMS["vsd_auth"]["api_version"]))
        mock_vspk.NUVSDSession.assert_called_with(username=TEST_PARAMS["vsd_auth"]["username"],
                                                  password=TEST_PARAMS["vsd_auth"]["password"],
                                                  enterprise=TEST_PARAMS["vsd_auth"]["enterprise"],
                                                  api_url=TEST_PARAMS["vsd_auth"]["api_url"])
        mock_session.start.assert_called_with()
        mock_module.fail_json.assert_called_once_with(
            msg="Could not establish connection to VSD cannot connect")

    @patch("importlib.import_module")
    @patch("time.time")
    @patch(MODULE_PATCH)
    def test__no_licenses(self, module_patch, time_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)

        self.setup_licenses(mock_root, [])

        time_patch.return_value = SECONDS_PER_DAY
        main()

        test_days_left_dict = {}
        test_valid_dict = {}

        test_result_dict = {"validity": test_valid_dict, "days_left": test_days_left_dict}

        self.validate_session(import_patch)
        mock_module.exit_json.assert_called_once_with(changed=False,
                                                      result=test_result_dict)

    @patch("importlib.import_module")
    @patch("time.time")
    @patch(MODULE_PATCH)
    def test__bad_mode(self, module_patch, time_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        lic_1 = self.get_mock_license(SECONDS_PER_DAY * 366, 1, "lic1")
        lic_2 = self.get_mock_license(SECONDS_PER_DAY * 500, 0, "lic2")

        self.setup_licenses(mock_root, [lic_1, lic_2])

        time_patch.return_value = SECONDS_PER_DAY
        main()

        test_days_left_dict = {lic_1.unique_license_identifier: [365, lic_1.licensed_feature], lic_2.unique_license_identifier: [499, lic_2.licensed_feature]}
        test_valid_dict = {lic_1.unique_license_identifier: True, lic_2.unique_license_identifier: False}

        test_result_dict = {"validity": test_valid_dict, "days_left": test_days_left_dict}

        self.validate_session(import_patch)
        mock_module.exit_json.assert_called_once_with(changed=False,
                                                      result=test_result_dict)

    @patch("importlib.import_module")
    @patch("time.time")
    @patch(MODULE_PATCH)
    def test__will_expire(self, module_patch, time_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        lic_1 = self.get_mock_license(SECONDS_PER_DAY * 365, 1, "lic1")
        lic_2 = self.get_mock_license(SECONDS_PER_DAY * 500, 0, "lic2")

        self.setup_licenses(mock_root, [lic_1, lic_2])

        time_patch.return_value = SECONDS_PER_DAY
        main()

        self.validate_session(import_patch)
        mock_module.fail_json.assert_called_once_with(
            msg="VSD License will expire in 364 days")

    @patch("importlib.import_module")
    @patch("time.time")
    @patch(MODULE_PATCH)
    def test__has_expired(self, module_patch, time_patch, import_patch):
        mock_module = self.setup_module(module_patch)
        mock_root = self.setup_session_root(import_patch)
        lic_1 = self.get_mock_license(SECONDS_PER_DAY - 1, 1, "lic1")
        lic_2 = self.get_mock_license(SECONDS_PER_DAY * 500, 0, "lic2")

        self.setup_licenses(mock_root, [lic_1, lic_2])

        time_patch.return_value = SECONDS_PER_DAY
        main()

        self.validate_session(import_patch)
        mock_module.fail_json.assert_called_once_with(
            msg="The VSD License has expired, please renew the License before proceeding to install the VSD image")
