import datetime
import uuid
from threading import Event

import mock

from svc.constants.home_automation import Automation
from svc.constants.lights_state import LightState, LightAlarmState
from svc.constants.settings_state import Settings


@mock.patch('svc.constants.lights_state.create_thread')
@mock.patch('svc.constants.lights_state.get_light_api_key')
class TestLightState:
    GROUP_ID = 4
    API_KEY = 'abc123'
    DAYS = 'MonTueWed'
    TASK_ID = str(uuid.uuid4())
    TIME = datetime.time.fromisoformat('00:00:01')

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.STATE = LightState.get_instance()
        self.STATE.LIGHT_ALARMS = []

    @mock.patch('svc.constants.lights_state.LightAlarmState')
    def test_add_light_alarm__should_create_the_light_thread(self, mock_light, mock_api, mock_thread):
        alarm = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        mock_light.return_value = alarm
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)

        mock_thread.assert_called_with(alarm, mock.ANY, Automation.TIME.TEN_SECONDS)

    def test_add_light_alarm__should_not_create_thread_when_it_already_exists(self, mock_api, mock_thread):
        alarm = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)

        mock_thread.assert_not_called()

    def test_add_light_alarm__should_create_thread_when_other_non_matching_threads(self, mock_api, mock_thread):
        alarm = LightAlarmState(str(uuid.uuid4()), self.GROUP_ID, self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)

        mock_thread.assert_called()

    def test_remove_light_alarm__should_remove_item_from_list_with_matching_task_id(self, mock_api, mock_thread):
        event = mock.create_autospec(Event)
        alarm = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        alarm.STOP_EVENT = event
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.remove_light_alarm(self.TASK_ID)

        assert self.STATE.LIGHT_ALARMS == []

    def test_remove_light_alarm__should_not_remove_item_from_list_with_different_task_id(self, mock_api, mock_thread):
        alarm = LightAlarmState(str(uuid.uuid4()), self.GROUP_ID, self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.remove_light_alarm(self.TASK_ID)

        assert self.STATE.LIGHT_ALARMS == [alarm]

    def test_remove_light_alarm__should_stop_matching_alarms(self, mock_api, mock_thread):
        event = mock.create_autospec(Event)
        alarm = LightAlarmState(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS)
        alarm.STOP_EVENT = event
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.remove_light_alarm(self.TASK_ID)

        event.set.assert_called()

    def test_get_light_api_key__should_return_cached_api_key(self, mock_api, mock_thread):
        self.STATE.API_KEY = self.API_KEY
        actual = self.STATE.get_light_api_key()

        assert actual == self.API_KEY

    def test_get_light_api_key__should_make_call_to_get_key_when_not_cached(self, mock_api, mock_thread):
        self.STATE.API_KEY = None
        self.STATE.get_light_api_key()

        mock_api.assert_called_with(self.SETTINGS.light_api_user, self.SETTINGS.light_api_password)

    def test_get_light_api_key__should_not_create_alarm_when_group_id_is_none(self, mock_api, mock_thread):
        self.STATE.add_light_alarm(None, self.TIME, self.DAYS)

        assert len(self.STATE.LIGHT_ALARMS) == 0

    def test_get_light_api_key__should_not_create_alarm_when_alarm_time_is_none(self, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.GROUP_ID, None, self.DAYS)

        assert len(self.STATE.LIGHT_ALARMS) == 0
