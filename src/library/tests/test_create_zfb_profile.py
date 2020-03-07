from library.create_zfb_profile import is_license_already_installed, main
from mock import call, patch, MagicMock
import os

LICENSE_FILE = os.path.join(os.path.dirname(__file__), "mock_license.txt")
LICENSE_ID = "01234567890ABCDEKLMNOPQRSTUVWXYZ"
MODULE_PATCH = "library.create_zfb_profile.AnsibleModule"
VSPK_PATCH = "library.create_zfb_profile.VSPK"
TEST_PARAMS = {
    "nsgv_path": "/tmp/ansible.1234",
    "fact_name": "nsgv_already_configured",
    "vsd_license_file": LICENSE_FILE,
    "vsd_auth": {
        "username": "csproot",
        "password": "csproot",
        "enterprise": "csp",
        "api_url": "https://localhost:8443"},
    "zfb_constants": {
        "proxy_user": "proxy",
        "useTwoFactor": False,
        "upgradeAction": "NONE",
        "network_port_type": "NETWORK",
        "access_port_type": "ACCESS",
        "iso_params": {
            "mediaType": "ISO",
            "associatedEntityType": "nsgatewaytemplate",
            "NSGType": "ANY",
            "associatedEntityID": "update"}},
    "zfb_proxy_user": {
        "firstName": "John",
        "lastName": "Doe",
        "email": "user@email.com",
        "password": "pass"},
    "zfb_nsg": {
        "nsg_organization": "enterprise",
        "nsg_name": "NSG1",
        "nsg_template_name": "nsg_template",
        "match_type": "ip_address",
        "match_value": "192.168.1.1",
        "ssh_service": "DISABLED"},
    "zfb_ports": {
        "network_port": {
            "name": "port1_network",
            "physicalName": "port1"},
        "access_ports": [{
            "name": "port2_access",
            "physicalName": "port2",
            "VLANRange": "0-100",
            "vlan_value": 20}]},
    "zfb_nsg_infra": {
        "name": "nsg_infra",
        "proxyDNSName": "vnsutil1.example.com",
        "instanceSSHOverride": "ALLOWED"},
    "zfb_vsc_infra": {
        "name": "vsc_infra",
        "firstController": "192.168.1.100",
        "secondController": "192.168.1.101"}}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


class TestCreateZfbProfile(object):

    def setup_session(self, vspk_patch):

        self.mock_session = MagicMock()
        vspk_patch.NUVSDSession.return_value = self.mock_session
        self.mock_root = MagicMock()
        self.mock_session.user = self.mock_root

    def verify_session(self, vspk_patch):
        vspk_patch.NUVSDSession.assert_called_once_with(
            **TEST_PARAMS["vsd_auth"])
        self.mock_session.start.assert_called_once_with()

    def setup_license(self, vspk_patch):
        self.mock_root.licenses = MagicMock()
        self.mock_root.licenses.get.return_value = list()
        vspk_patch.NULicense.return_value = "test_license"

    def verify_license(self, vspk_patch):
        with open(LICENSE_FILE, "r") as f:
            vsd_license_str = f.read()

        vspk_patch.NULicense.assert_called_once_with(license=vsd_license_str)
        self.mock_root.create_child.assert_has_calls([call("test_license")])

    def setup_enterprise(self, vspk_patch):
        self.mock_root.enterprises.get_first.return_value = None
        self.mock_enterprise = MagicMock()
        vspk_patch.NUEnterprise.return_value = self.mock_enterprise

    def verify_enterprise(self, vspk_patch):
        vspk_patch.NUEnterprise.assert_has_calls([call(
            name=TEST_PARAMS["zfb_nsg"]["nsg_organization"])])
        self.mock_root.create_child.assert_has_calls(
            [call(self.mock_enterprise)])

    def verify_proxy_user(self, vspk_patch):
        vspk_patch.NUUser.assert_has_calls([call(
            first_name=TEST_PARAMS["zfb_proxy_user"]['firstName'],
            last_name=TEST_PARAMS["zfb_proxy_user"]['lastName'],
            user_name=TEST_PARAMS["zfb_constants"]['proxy_user'],
            email=TEST_PARAMS["zfb_proxy_user"]['email'],
            password=TEST_PARAMS["zfb_proxy_user"]['password'])])

    def setup_nsg_infra(self, vspk_patch):
        self.mock_nsg_infra = MagicMock()
        self.mock_nsg_infra.id = 9876
        vspk_patch.NUInfrastructureGatewayProfile.return_value = (
            self.mock_nsg_infra)
        self.mock_root.infrastructure_gateway_profiles.\
            get_first.return_value = None

    def verify_nsg_infra(self, vspk_patch):
        nsg_data = dict(TEST_PARAMS["zfb_nsg_infra"])
        nsg_data['useTwoFactor'] = TEST_PARAMS["zfb_constants"]["useTwoFactor"]
        nsg_data['upgradeAction'] = TEST_PARAMS["zfb_constants"][
            "upgradeAction"]
        vspk_patch.NUInfrastructureGatewayProfile.assert_called_once_with(
            data=nsg_data)
        self.mock_root.create_child.assert_has_calls(
            [call(self.mock_nsg_infra)])

    def setup_nsg_template(self, vspk_patch):
        self.mock_nsg_template = MagicMock()
        self.mock_nsg_template.id = 4567
        vspk_patch.NUNSGatewayTemplate.return_value = self.mock_nsg_template
        self.mock_root.ns_gateway_templates.get_first.return_value = None

    def verify_nsg_template(self, vspk_patch):
        vspk_patch.NUNSGatewayTemplate.assert_called_once_with(
            name=TEST_PARAMS["zfb_nsg"]["nsg_template_name"])
        self.mock_root.create_child.assert_has_calls(
            [call(self.mock_nsg_template)])
        assert (self.mock_nsg_template.infrastructure_profile_id ==
                self.mock_nsg_infra.id)

    def setup_vsc_infra(self, vspk_patch):
        self.mock_vsc_infra = MagicMock()
        vspk_patch.NUInfrastructureVscProfile.\
            return_value = self.mock_vsc_infra
        self.mock_root.infrastructure_vsc_profiles.\
            get_first.return_value = None

    def verify_vsc_infra(self, vspk_patch):
        vspk_patch.NUInfrastructureVscProfile.assert_called_once_with(
            data=TEST_PARAMS["zfb_vsc_infra"])
        self.mock_root.create_child.assert_has_calls(
            [call(self.mock_vsc_infra)])

    def setup_nsg_ports(self, vspk_patch):
        self.mock_network_port = MagicMock()
        self.mock_access_port = MagicMock()
        vspk_patch.NUNSPortTemplate.side_effect = [self.mock_network_port,
                                                   self.mock_access_port]
        self.mock_nsg_template.ns_port_templates.get_first.return_value = None

    def verify_nsg_ports(self, vspk_patch):
        network_data = dict(TEST_PARAMS["zfb_ports"]["network_port"])
        access_ports = list(TEST_PARAMS["zfb_ports"]["access_ports"])
        network_data["portType"] = TEST_PARAMS["zfb_constants"][
            "network_port_type"]
        vspk_patch.NUNSPortTemplate.assert_has_calls(
            [call(data=network_data)])
        self.mock_nsg_template.create_child.assert_has_calls(
            [call(self.mock_network_port)])

        for port in access_ports:
            vspk_patch.NUNSPortTemplate.assert_has_calls(
                [call(data=port)])
            self.mock_nsg_template.create_child.assert_has_calls(
                [call(self.mock_access_port)])

    def setup_nsg_device(self, vspk_patch):
        self.mock_nsg_device = MagicMock()
        vspk_patch.NUNSGateway.return_value = self.mock_nsg_device
        self.mock_enterprise.ns_gateways.get_first.return_value = None

    def verify_nsg_device(self, vspk_patch):
        nsg_data = {"name": TEST_PARAMS["zfb_nsg"]['nsg_name'],
                    "templateID": self.mock_nsg_template.id,
                    "ZFBMatchAttribute": TEST_PARAMS["zfb_nsg"]['match_type'],
                    "ZFBMatchValue": TEST_PARAMS["zfb_nsg"]['match_value'],
                    "personality": "NSG",
                    "SSHService": TEST_PARAMS["zfb_nsg"]['ssh_service']}
        vspk_patch.NUNSGateway.assert_called_once_with(data=nsg_data)
        self.mock_enterprise.create_child.assert_has_calls(
            [call(self.mock_nsg_device)])

    def setup_create_iso(self, vspk_patch):
        self.mock_job = MagicMock()
        self.mock_job.result = "MOCK DATA"
        vspk_patch.NUJob.return_value = self.mock_job

    def verify_create_iso(self, vspk_patch):
        assert self.mock_job.command == "GET_ZFB_INFO"
        parameters = dict(TEST_PARAMS["zfb_constants"]["iso_params"])
        parameters["associatedEntityID"] = self.mock_nsg_template.id
        assert self.mock_job.parameters == parameters
        self.mock_enterprise.create_child.assert_has_calls(
            [call(self.mock_job)])

    def verify_subproc(self, mock_subproc):
        mock_subproc.assert_has_calls(
            [call("echo MOCK DATA | base64 -d > "
                  "/tmp/ansible.1234/user_image.iso.gz",
                  shell=True),
             call("gzip -f -d /tmp/ansible.1234/user_image.iso.gz",
                  shell=True)])

    @patch(MODULE_PATCH)
    @patch(VSPK_PATCH)
    @patch("subprocess.call")
    def test_iso_create__success(self, mock_subproc, vspk_patch, module_patch):
        mock_module = setup_module(module_patch)
        self.setup_session(vspk_patch)
        self.setup_license(vspk_patch)
        self.setup_enterprise(vspk_patch)
        self.setup_nsg_infra(vspk_patch)
        self.setup_nsg_template(vspk_patch)
        self.setup_vsc_infra(vspk_patch)
        self.setup_nsg_ports(vspk_patch)
        self.setup_nsg_device(vspk_patch)
        self.setup_create_iso(vspk_patch)

        main()

        self.verify_session(vspk_patch)
        self.verify_license(vspk_patch)
        self.verify_enterprise(vspk_patch)
        self.verify_proxy_user(vspk_patch)
        self.verify_nsg_infra(vspk_patch)
        self.verify_nsg_template(vspk_patch)
        self.verify_vsc_infra(vspk_patch)
        self.verify_nsg_ports(vspk_patch)
        self.verify_nsg_device(vspk_patch)
        self.verify_create_iso(vspk_patch)
        self.verify_subproc(mock_subproc)

        mock_module.fail_json.assert_not_called()
        mock_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts={"nsgv_already_configured": False})

    def test_license__installed(self):
        with open(LICENSE_FILE, "r") as f:
            vsd_license_str = f.read()

        vsd_license = MagicMock()
        vsd_license.unique_license_identifier = LICENSE_ID
        bogus_license = MagicMock()
        bogus_license.unique_license_identifier = "asdfasdf"

        licenses = [bogus_license]

        mock_root = MagicMock()
        mock_root.licenses = MagicMock()
        mock_root.licenses.get.return_value = licenses

        assert is_license_already_installed(mock_root,
                                            vsd_license_str) is False

        licenses.append(vsd_license)

        assert is_license_already_installed(mock_root,
                                            vsd_license_str) is True

    @patch(MODULE_PATCH)
    def test__bad_license(self, module_patch):
        params = dict(TEST_PARAMS)
        params["vsd_license_file"] = "invalid_file.bad"
        mock_module = setup_module(module_patch, params)

        main()

        mock_module.fail_json.assert_called_once()
        args, kwargs = mock_module.fail_json.call_args_list[0]
        assert "ERROR: Failure reading file: " in kwargs["msg"]

    @patch(MODULE_PATCH)
    @patch(VSPK_PATCH)
    def test__cannot_connect(self, vspk_patch, module_patch):
        mock_module = setup_module(module_patch)

        mock_session = MagicMock()
        vspk_patch.NUVSDSession.return_value = mock_session
        mock_session.start.side_effect = Exception("Test")

        main()

        mock_module.fail_json.assert_called_once()
        args, kwargs = mock_module.fail_json.call_args_list[0]
        assert "ERROR: Could not establish connection to VSD" in kwargs["msg"]
