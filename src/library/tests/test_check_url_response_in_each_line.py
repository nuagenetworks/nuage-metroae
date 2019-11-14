from library.check_url_response_in_each_line import main
from mock import call, patch, MagicMock

MODULE_PATCH = "library.check_url_response_in_each_line.AnsibleModule"
TEST_PARAMS = {
    "url": "http://localhost",
    "timeout_seconds": 15,
    "test_interval_seconds": 5,
    "search_string": "TEST"
}


def setup_module(module_patch, params=None):
    mock_module = MagicMock()
    module_patch.return_value = mock_module
    if params is None:
        mock_module.params = TEST_PARAMS
    else:
        mock_module.params = params

    return mock_module


@patch("requests.get")
@patch("time.sleep")
@patch(MODULE_PATCH)
def test_normal__success(module_patch, sleep_patch, requests_patch):
    mock_module = setup_module(module_patch)
    sleep_patch.return_value = None

    test_response = "TEST string\nat end TEST"

    mock_resp = MagicMock()
    mock_resp.text = test_response
    requests_patch.return_value = mock_resp

    main()

    requests_patch.assert_called_once_with(TEST_PARAMS["url"])
    sleep_patch.assert_not_called()
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(changed=True,
                                                  response=test_response)


@patch("requests.get")
@patch("time.sleep")
@patch(MODULE_PATCH)
def test_wait__success(module_patch, sleep_patch, requests_patch):
    mock_module = setup_module(module_patch)
    sleep_patch.return_value = None

    not_present_response = "Not yet\nat end TEST"
    test_response = "TEST string\nat end TEST"

    mock_resp_1 = MagicMock()
    mock_resp_1.text = not_present_response
    mock_resp_2 = MagicMock()
    mock_resp_2.text = test_response
    requests_patch.side_effect = [mock_resp_1, mock_resp_2]

    main()

    requests_patch.assert_has_calls([call(TEST_PARAMS["url"]),
                                     call(TEST_PARAMS["url"])])
    sleep_patch.assert_called_once_with(TEST_PARAMS['test_interval_seconds'])
    mock_module.fail_json.assert_not_called()
    mock_module.exit_json.assert_called_once_with(changed=True,
                                                  response=test_response)


@patch("requests.get")
@patch("time.sleep")
@patch(MODULE_PATCH)
def test__timeout(module_patch, sleep_patch, requests_patch):
    mock_module = setup_module(module_patch)
    sleep_patch.return_value = None

    test_response = "Not in here\nat end TEST"

    mock_resp = MagicMock()
    mock_resp.text = test_response
    requests_patch.return_value = mock_resp

    main()

    requests_patch.assert_has_calls([call(TEST_PARAMS["url"]),
                                     call(TEST_PARAMS["url"]),
                                     call(TEST_PARAMS["url"])])
    sleep_patch.assert_has_calls([call(TEST_PARAMS['test_interval_seconds']),
                                  call(TEST_PARAMS['test_interval_seconds']),
                                  call(TEST_PARAMS['test_interval_seconds'])])
    msg = ("Did not find the search string %s from response"
           " %s within %i seconds") % (TEST_PARAMS["search_string"],
                                       test_response,
                                       TEST_PARAMS["timeout_seconds"])
    mock_module.fail_json.assert_called_once_with(msg=msg)
