from mock import patch

from svc.services.api_service import update_light_groups


@patch('svc.services.api_service.api_utils')
class TestApiService:
    API_KEY = 'asjdfhasiw'
    GROUP_ID = '2'
    ALL_GROUPS_ID = 'ALL'
    ON_STATE = True
    OFF_STATE = False

    def test_update_light_groups__should_call_to_get_light_groups_when_all_group_id(self, mock_api):
        update_light_groups(self.API_KEY, self.ALL_GROUPS_ID, self.ON_STATE)

        mock_api.get_light_groups.assert_called_with(self.API_KEY)

    def test_update_light_groups__should_not_call_to_get_light_groups_when_single_group_id(self, mock_api):
        update_light_groups(self.API_KEY, self.GROUP_ID, self.ON_STATE)

        mock_api.get_light_groups.assert_not_called()

    def test_update_light_groups__should_call_to_get_light_groups_when_all_group_id_case_insensitive(self, mock_api):
        update_light_groups(self.API_KEY, 'all', self.ON_STATE)

        mock_api.get_light_groups.assert_called_with(self.API_KEY)

    def test_update_light_groups__should_call_to_set_all_light_groups_when_all_group_id_and_on_requested(self, mock_api):
        mock_api.get_light_groups.return_value = {'1': {'name': 'Living Room'}, '2': {'name': 'Kitchen'}}
        update_light_groups(self.API_KEY, self.ALL_GROUPS_ID, self.ON_STATE)

        assert mock_api.set_light_groups.call_count == 2
        mock_api.set_light_groups.assert_any_call(self.API_KEY, '1', True, 255)
        mock_api.set_light_groups.assert_any_call(self.API_KEY, '2', True, 255)

    def test_update_light_groups__should_call_to_set_all_light_groups_when_all_group_id_and_off_requested(self, mock_api):
        mock_api.get_light_groups.return_value = {'1': {'name': 'Living Room'}, '2': {'name': 'Kitchen'}}
        update_light_groups(self.API_KEY, self.ALL_GROUPS_ID, self.OFF_STATE)

        assert mock_api.set_light_groups.call_count == 2
        mock_api.set_light_groups.assert_any_call(self.API_KEY, '1', False, 0)
        mock_api.set_light_groups.assert_any_call(self.API_KEY, '2', False, 0)
