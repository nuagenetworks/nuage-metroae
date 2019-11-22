from library.nuage_append import main
from mock import patch, MagicMock
import os

MODULE_PATCH = "library.nuage_append.AnsibleModule"
TEST_PARAMS = {
    "filename": "/tmp/ansible_pytest.txt",
    "text": "{\"taxes owed\": \"0.00\"}"
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

    if os.path.isfile(TEST_PARAMS["filename"]):
        os.remove(TEST_PARAMS["filename"])

    open(TEST_PARAMS["filename"], "a").close()

    main()

    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(changed=True)

    with open(TEST_PARAMS["filename"], "r") as f:
        contents = f.read()

    assert contents == TEST_PARAMS["text"]

    params = dict(TEST_PARAMS)
    params["text"] = "append string"

    mock_module = setup_module(module_patch, params)

    main()

    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(changed=True)

    with open(TEST_PARAMS["filename"], "r") as f:
        contents = f.read()

    assert contents == TEST_PARAMS["text"] + "append string"

    os.remove(TEST_PARAMS["filename"])
