import datetime

from mock import patch

from svc.constants.lights_state import LightAlarm
from svc.constants.settings_state import Settings
from svc.services.light_service import create_light_alarm


@patch('svc.services.light_service.LightState')
@patch('svc.services.light_service.get_light_preferences_by_user')
class TestLightService:
    DAYS = 'MonTue'
    USER_ID = 'def098'
    GROUP_ID = 'abc123'
    TIME = datetime.time()

    def setup_method(self):
        self.ALARM = LightAlarm(self.GROUP_ID, self.TIME, self.DAYS)
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'UserId': self.USER_ID}

    def test_create_light_alarm__should_make_call_to_get_light_preferences(self, mock_pref, mock_light):
        create_light_alarm()

        mock_pref.assert_called_with(self.USER_ID)

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_time_none(self, mock_pref, mock_light):
        mock_pref.return_value = {'alarm_time': None, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID}
        create_light_alarm()

        mock_light.get_instance.return_value.add_replace_light_alarm.assert_not_called()

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_days_none(self, mock_pref, mock_light):
        mock_pref.return_value = {'alarm_time': self.TIME, 'alarm_days': None, 'alarm_light_group': self.GROUP_ID}
        create_light_alarm()

        mock_light.get_instance.return_value.add_replace_light_alarm.assert_not_called()

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_group_id_none(self, mock_pref, mock_light):
        mock_pref.return_value = {'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': None}
        create_light_alarm()

        mock_light.get_instance.return_value.add_replace_light_alarm.assert_not_called()

    def test_create_light_alarm__should_call_add_replace_alarm(self, mock_pref, mock_light):
        light_pref = {'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID}
        mock_pref.return_value = light_pref
        create_light_alarm()

        mock_light.get_instance.return_value.add_replace_light_alarm.assert_called_with(light_pref['alarm_light_group'], light_pref['alarm_time'], light_pref['alarm_days'])
