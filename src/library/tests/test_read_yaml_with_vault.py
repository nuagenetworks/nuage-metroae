from library.read_yaml_with_vault import main
from mock import patch, MagicMock
import os

MODULE_PATCH = "library.read_yaml_with_vault.AnsibleModule"
YAML_PATCH = "library.read_yaml_with_vault.yaml"
TEST_PARAMS = {
    "path": os.path.join(os.path.dirname(__file__), "mock_encrypted.yml"),
    "fact_name": "encrypted"
}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


@patch(MODULE_PATCH)
def test__success(module_patch):
    mock_module = setup_module(module_patch)

    main()

    mock_module.fail_json.assert_not_called()
    assert mock_module.exit_json.call_count == 1
    args, kwargs = mock_module.exit_json.call_args_list[0]

    parsed_yaml = kwargs["ansible_facts"][TEST_PARAMS["fact_name"]]
    assert parsed_yaml["username"] == "username"
    assert "!vault" in parsed_yaml["password"]


@patch(YAML_PATCH)
@patch(MODULE_PATCH)
def test__parse_error(module_patch, yaml_patch):
    mock_module = setup_module(module_patch)
    yaml_patch.load.side_effect = Exception("Test exception")

    main()

    mock_module.fail_json.assert_called_once_with(
        msg="Could not load yaml file %s: %s" % (
            TEST_PARAMS["path"], "Test exception"))
