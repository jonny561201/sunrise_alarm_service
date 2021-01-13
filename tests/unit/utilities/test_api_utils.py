import json

from mock import patch, ANY
from requests import ReadTimeout, Response

from svc.constants.home_automation import Automation
from svc.utilities.api_utils import set_light_groups, get_light_api_key


@patch('svc.utilities.api_utils.requests')
class TestLightApiRequests:
    USERNAME = 'fake username'
    PASSWORD = 'fake password'
    BASE_URL = 'http://192.168.1.142:80/api'
    API_KEY = 'fake api key'
    LIGHT_API = None

    def test_get_light_api_key__should_call_requests_with_url(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        mock_requests.post.assert_called_with(self.BASE_URL, data=ANY, headers=ANY, timeout=ANY)

    def test_get_light_api_key__should_call_requests_with_device_type(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        body = json.dumps({'devicetype': Automation().APP_NAME})
        mock_requests.post.assert_called_with(ANY, data=body, headers=ANY, timeout=ANY)

    def test_get_light_api_key__should_provide_username_and_pass_as_auth_header(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        headers = {'Authorization': 'Basic ' + 'ZmFrZSB1c2VybmFtZTpmYWtlIHBhc3N3b3Jk'}
        mock_requests.post.assert_called_with(ANY, data=ANY, headers=headers, timeout=ANY)

    def test_get_light_api_key__should_call_requests_with_timeout_at_five(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        mock_requests.post.assert_called_with(ANY, data=ANY, headers=ANY, timeout=5)

    def test_get_light_api_key__should_return_api_key_response(self, mock_requests):
        response_data = [{'success': {'username': self.API_KEY}}]
        mock_requests.post.return_value = self.__create_response(data=response_data)

        actual = get_light_api_key(self.USERNAME, self.PASSWORD)

        assert actual == self.API_KEY

    def test_get_light_api_key__should_return_none_when_exception(self, mock_requests):
        mock_requests.post.side_effect = ReadTimeout()
        actual = get_light_api_key(self.USERNAME, self.PASSWORD)

        assert actual is None

    def test_set_light_groups__should_call_state_url(self, mock_requests):
        group_id = 1
        expected_url = self.BASE_URL + '/%s/groups/%s/action' % (self.API_KEY, group_id)
        set_light_groups(self.API_KEY, group_id, True)

        mock_requests.put.assert_called_with(expected_url, data=ANY)

    def test_set_light_groups__should_call_state_with_on_off_set(self, mock_requests):
        state = False
        set_light_groups(self.API_KEY, 2, state)

        expected_request = json.dumps({'on': state})
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    def test_set_light_groups__should_call_state_with_dimmer_value(self, mock_requests):
        state = True
        brightness = 233
        set_light_groups(self.API_KEY, 1, state, brightness)

        expected_request = json.dumps({'on': state, 'bri': brightness})
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    def test_set_light_groups__should_call_state_with_on_set_true_if_dimmer_value(self, mock_requests):
        brightness = 155
        set_light_groups(self.API_KEY, 1, False, brightness)

        expected_request = json.dumps({'on': True, 'bri': brightness})
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    @staticmethod
    def __create_response(status=200, data=[]):
        response = Response()
        response.status_code = status
        response._content = json.dumps(data).encode('UTF-8')
        return response