import datetime
import uuid

from mock import patch

from svc.constants.lights_state import LightAlarmState
from svc.constants.settings_state import Settings
from svc.services.light_service import create_light_alarm


@patch('svc.services.light_service.LightState')
@patch('svc.services.light_service.get_light_tasks_by_user')
class TestLightService:
    DAYS = 'MonTue'
    USER_ID = 'def098'
    GROUP_ID = 'abc123'
    TIME = datetime.time()
    TASK_ID = str(uuid.uuid4())

    def setup_method(self):
        self.ALARM = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'UserId': self.USER_ID}

    def test_create_light_alarm__should_make_call_to_get_light_preferences(self, mock_tasks, mock_light):
        create_light_alarm()

        mock_tasks.assert_called_with(self.USER_ID)

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_time_none(self, mock_tasks, mock_light):
        mock_tasks.return_value = [{'alarm_time': None, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID, 'task_id': self.TASK_ID}]
        create_light_alarm()

        mock_light.get_instance.return_value.add_light_alarm.assert_not_called()

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_days_none(self, mock_tasks, mock_light):
        mock_tasks.return_value = [{'alarm_time': self.TIME, 'alarm_days': None, 'alarm_light_group': self.GROUP_ID, 'task_id': self.TASK_ID}]
        create_light_alarm()

        mock_light.get_instance.return_value.add_light_alarm.assert_not_called()

    def test_create_light_alarm__should_not_call_add_replace_alarm_when_alarm_group_id_none(self, mock_tasks, mock_light):
        mock_tasks.return_value = [{'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': None, 'task_id': self.TASK_ID}]
        create_light_alarm()

        mock_light.get_instance.return_value.add_light_alarm.assert_not_called()

    def test_create_light_alarm__should_call_add_alarm(self, mock_tasks, mock_light):
        light_pref = {'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID, 'task_id': self.TASK_ID}
        mock_tasks.return_value = [light_pref]
        create_light_alarm()

        mock_light.get_instance.return_value.add_light_alarm.assert_called_with(self.TASK_ID, light_pref['alarm_light_group'], light_pref['alarm_time'], light_pref['alarm_days'])

    def test_create_light_alarm__should_call_remove_light_on_items_missing_from_api_response(self, mock_tasks, mock_light):
        other_task = str(uuid.uuid4())
        missing_task = str(uuid.uuid4())
        pref_one = {'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID, 'task_id': self.TASK_ID}
        pref_two = {'alarm_time': self.TIME, 'alarm_days': self.DAYS, 'alarm_light_group': self.GROUP_ID, 'task_id': other_task}
        alarm_one = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        alarm_two = LightAlarmState(other_task, self.GROUP_ID, self.TIME, self.DAYS)
        alarm_three = LightAlarmState(missing_task, self.GROUP_ID, self.TIME, self.DAYS)
        mock_light.get_instance.return_value.LIGHT_ALARMS = [alarm_one, alarm_two, alarm_three]
        mock_tasks.return_value = [pref_one, pref_two]
        create_light_alarm()

        mock_light.get_instance.return_value.remove_light_alarm.assert_called_with(missing_task)

    def test_create_light_alarm__should_not_fail_when_api_call_returns_empty_list(self, mock_tasks, mock_light):
        mock_tasks.return_value = []
        mock_light.get_instance.return_value.LIGHT_ALARMS = []
        create_light_alarm()

        mock_light.get_instance.return_value.add_light_alarm.assert_not_called()
        mock_light.get_instance.return_value.remove_light_alarm.assert_not_called()

    @patch('svc.services.light_service.logging')
    def test_create_light_alarm__should_log_when_exception(self, mock_log, mock_tasks, mock_light):
        error = TimeoutError()
        mock_tasks.side_effect = error
        create_light_alarm()

        mock_log.error.assert_called_with(error)
