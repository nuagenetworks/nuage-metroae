from library.validate_against_schema import main
from mock import patch, MagicMock
import os

MODULE_PATCH = "library.validate_against_schema.AnsibleModule"
YAML_PATCH = "library.validate_against_schema.yaml"
TEST_PARAMS = {
    "path": os.path.join(os.path.dirname(__file__), "mock_encrypted.yml"),
    "schema": os.path.join(os.path.dirname(__file__), "mock_schema.json")
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


@patch(YAML_PATCH)
@patch(MODULE_PATCH)
def test__data_parse_error(module_patch, yaml_patch):
    mock_module = setup_module(module_patch)
    yaml_patch.load.side_effect = Exception("Bad yaml")

    main()

    mock_module.fail_json.assert_called_once_with(
        msg="Could not load yaml file %s: %s" % (
            TEST_PARAMS["path"], "Bad yaml"))


@patch(YAML_PATCH)
@patch(MODULE_PATCH)
def test__schema_parse_error(module_patch, yaml_patch):
    mock_module = setup_module(module_patch)
    yaml_patch.safe_load.side_effect = Exception("Bad schema")

    main()

    mock_module.fail_json.assert_called_once_with(
        msg="Could not load schema %s: %s" % (
            TEST_PARAMS["schema"], "Bad schema"))


@patch(MODULE_PATCH)
def test__schema_error(module_patch):
    params = dict(TEST_PARAMS)
    params["schema"] = os.path.join(os.path.dirname(__file__),
                                    "mock_bad_schema.json")
    mock_module = setup_module(module_patch, params)

    main()

    mock_module.fail_json.assert_called_once_with(
        msg="Invalid data in %s for Username: %s" % (
            TEST_PARAMS["path"], "'username' is not of type 'integer'"))
