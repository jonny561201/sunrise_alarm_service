from mock import patch

from svc.services.api_service import update_light_groups


@patch('svc.services.api_service.get_light_groups')
class TestApiService:
    API_KEY = 'asjdfhasiw'
    GROUP_ID = '2'
    ALL_GROUPS_ID = 'ALL'
    ON_STATE = True
    OFF_STATE = False

    def test_update_light_groups__should_call_to_set_light_groups_when_all_group_id(self, mock_api):
        update_light_groups(self.API_KEY, self.ALL_GROUPS_ID, self.ON_STATE)

        mock_api.assert_called_with(self.API_KEY)

    def test_update_light_groups__should_not_call_to_set_light_groups_when_single_group_id(self, mock_api):
        update_light_groups(self.API_KEY, self.GROUP_ID, self.ON_STATE)

        mock_api.assert_not_called()