from library.yaml_checker import main
from mock import patch, MagicMock
import os

MODULE_PATCH = "library.yaml_checker.AnsibleModule"
TEST_PARAMS = {
    "path": os.path.join(os.path.dirname(__file__), "mock_encrypted.yml")
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
    mock_module.exit_json.assert_called_once_with(changed=False)


@patch(MODULE_PATCH)
def test__invalid_yaml(module_patch):
    params = dict(TEST_PARAMS)
    params["path"] = os.path.join(os.path.dirname(__file__),
                                  "invalid_yaml.yml")

    mock_module = setup_module(module_patch, params)

    main()

    assert mock_module.fail_json.call_count == 1
    args, kwargs = mock_module.fail_json.call_args_list[0]
    assert "YAML Syntax Error" in kwargs["msg"]
    assert "invalid_yaml.yml" in kwargs["msg"]
    assert "line 2, column 1" in kwargs["msg"]


@patch(MODULE_PATCH)
def test__duplicate_keys(module_patch):
    params = dict(TEST_PARAMS)
    params["path"] = os.path.join(os.path.dirname(__file__),
                                  "duplicate_keys.yml")

    mock_module = setup_module(module_patch, params)

    main()

    mock_module.fail_json.assert_called_once_with(
        msg="'Duplicate Variable Found - duplicate'")
