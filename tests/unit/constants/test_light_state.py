import datetime
import uuid
from threading import Event

import mock

from svc.constants.home_automation import Automation
from svc.constants.lights_state import LightState, LightAlarmState
from svc.constants.settings_state import Settings
from svc.utilities.event_utils import MyThread


@mock.patch('svc.constants.lights_state.create_thread')
@mock.patch('svc.constants.lights_state.get_light_api_key')
class TestLightState:
    GROUP_ID = '4'
    API_KEY = 'abc123'
    DAYS = 'MonTueWed'
    TASK_TYPE = 'sunrise alarm'
    TASK_ID = str(uuid.uuid4())
    TIME = datetime.time.fromisoformat('00:00:01')

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.STATE = LightState.get_instance()
        self.STATE.LIGHT_ALARMS = []

    @mock.patch('svc.constants.lights_state.LightAlarmState')
    def test_add_light_alarm__should_create_the_light_alarm_thread(self, mock_light, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, self.TASK_TYPE)

        mock_thread.assert_called_with(mock.ANY, Automation.TIME.TEN_SECONDS)
        mock_light.assert_called()

    @mock.patch('svc.constants.lights_state.LightOnOffState')
    def test_add_light_alarm__should_create_the_light_thread_for_turn_on(self, mock_light, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn on')

        mock_thread.assert_called_with(mock.ANY, Automation.TIME.TWENTY_SECONDS)
        mock_light.assert_called()

    def test_add_light_alarm__should_store_the_thread_on_the_alarm_list_for_turn_on(self, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn on')

        assert len(self.STATE.LIGHT_ALARMS) == 1

    def test_add_light_alarm__should_start_the_newly_created_thread_for_turn_on(self, mock_api, mock_thread):
        mock_alarm = mock.create_autospec(MyThread)
        mock_thread.return_value = mock_alarm
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn on')

        mock_alarm.start.assert_called()

    @mock.patch('svc.constants.lights_state.LightOnOffState')
    def test_add_light_alarm__should_create_the_light_thread_for_turn_off(self, mock_light, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn off')

        mock_thread.assert_called_with(mock.ANY, Automation.TIME.TWENTY_SECONDS)
        mock_light.assert_called()

    def test_add_light_alarm__should_store_the_thread_on_the_alarm_list_for_turn_off(self, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn off')

        assert len(self.STATE.LIGHT_ALARMS) == 1

    def test_add_light_alarm__should_start_the_newly_created_thread_for_turn_off(self, mock_api, mock_thread):
        mock_alarm = mock.create_autospec(MyThread)
        mock_thread.return_value = mock_alarm
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, 'turn off')

        mock_alarm.start.assert_called()

    def test_add_light_alarm__should_not_create_thread_when_it_already_exists(self, mock_api, mock_thread):
        alarm = LightAlarmState(self.TASK_ID, self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, self.TASK_TYPE)

        mock_thread.assert_not_called()

    def test_add_light_alarm__should_create_thread_when_other_non_matching_threads(self, mock_api, mock_thread):
        alarm = LightAlarmState(str(uuid.uuid4()), self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, self.TASK_TYPE)

        mock_thread.assert_called()

    def test_add_light_alarm__should_store_the_thread_on_the_alarm_list_for_sunrise(self, mock_api, mock_thread):
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, self.TASK_TYPE)

        assert len(self.STATE.LIGHT_ALARMS) == 1

    def test_add_light_alarm__should_start_the_newly_created_thread(self, mock_api, mock_thread):
        mock_alarm = mock.create_autospec(MyThread)
        mock_thread.return_value = mock_alarm
        self.STATE.add_light_alarm(self.TASK_ID, self.GROUP_ID, self.TIME, self.DAYS, self.TASK_TYPE)

        mock_alarm.start.assert_called()

    def test_remove_light_alarm__should_remove_item_from_list_with_matching_task_id(self, mock_api, mock_thread):
        event = mock.create_autospec(Event)
        my_alarm = mock.create_autospec(MyThread)
        my_alarm.stopped = event
        alarm = LightAlarmState(self.TASK_ID, self.TIME, self.DAYS)
        alarm.ACTIVE_THREAD = my_alarm
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.remove_light_alarm(self.TASK_ID)

        assert self.STATE.LIGHT_ALARMS == []

    def test_remove_light_alarm__should_not_remove_item_from_list_with_different_task_id(self, mock_api, mock_thread):
        alarm = LightAlarmState(str(uuid.uuid4()), self.TIME, self.DAYS)
        self.STATE.LIGHT_ALARMS.append(alarm)
        self.STATE.remove_light_alarm(self.TASK_ID)

        assert self.STATE.LIGHT_ALARMS == [alarm]

    def test_remove_light_alarm__should_stop_matching_alarms(self, mock_api, mock_thread):
        event = mock.create_autospec(Event)
        my_alarm = mock.create_autospec(MyThread)
        my_alarm.stopped = event
        alarm = LightAlarmState(self.TASK_ID, self.TIME, self.DAYS)
        alarm.ACTIVE_THREAD = my_alarm
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
