import datetime

from mock import patch

from svc.constants.lights_state import LightAlarmState
from svc.constants.thread_state import LightOnOffState
from svc.utilities.light_utils import light_alarm_program, light_on_program, light_off_program


@patch('svc.utilities.light_utils.time')
@patch('svc.utilities.light_utils.datetime')
@patch('svc.utilities.light_utils.set_light_groups')
class TestLightUtils:
    GROUP_ID = '3'
    TASK_ID = 'abc123'
    DAYS = 'MonTueFri'
    API_KEY = 'test_api_key'
    START_TIME = datetime.time(7, 30, 0)
    END_TIME = datetime.time(7, 40, 0)
    MONDAY = datetime.datetime(2020, 11, 2, 7, 34, 0)
    SUNDAY = datetime.datetime(2020, 11, 1, 7, 34, 0)
    WEDNESDAY = datetime.datetime(2020, 11, 4, 7, 34, 0)

    def setup_method(self):
        self.LIGHT_ON = LightOnOffState(self.TASK_ID, self.START_TIME, self.DAYS)
        self.ALARM = LightAlarmState(self.TASK_ID, self.START_TIME, self.DAYS)
        self.ALARM.BRIGHTNESS = 0
        self.ALARM.ALARM_START_TIME = self.START_TIME
        self.ALARM.ALARM_STOP_TIME = self.END_TIME

    def test_light_alarm_program__should_call_set_light_group_with_hue_and_zero_bri_first_time_if_after_start_time(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 31, 0)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 0, hue=3008, sat=255)

    def test_light_alarm_program__should_call_set_light_group_with_increased_bri_after_first_time_if_after_start_time(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 31, 0)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_any_call(self.API_KEY, self.GROUP_ID, 4, hue=3016, sat=255)

    def test_light_alarm_program__should_call_set_light_group_if_equal_start_time(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 30, 0)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 0, hue=3008, sat=255)

    def test_light_alarm_program__should_not_call_set_light_group_if_before_start_time(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 29, 0)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_alarm_program__should_not_call_set_light_group_if_after_end_time(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 41, 0)
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_alarm_program__should_increment_the_light_brightness(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.MONDAY
        self.ALARM.BRIGHTNESS = 4
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 16, hue=3008, sat=255)

    def test_light_alarm_program__should_max_out_brightness_at_255(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.MONDAY
        self.ALARM.BRIGHTNESS = 212
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 255, hue=3008, sat=255)

    def test_light_alarm_program__should_reset_the_light_state_value_back_to_zero(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = datetime.datetime(2020, 11, 2, 7, 41, 0)
        self.ALARM.ALARM_CURRENT_STATE = 203
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()
        assert self.ALARM.BRIGHTNESS == 0

    def test_light_alarm_program__should_call_set_light_when_greater_than_4100(self, mock_api, mock_date, mock_time):
        self.ALARM.HUE = 140
        mock_date.datetime.now.return_value = self.MONDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, self.ALARM.BRIGHTNESS, temp=2700, trans=4)

    def test_light_alarm_program__should_increment_brightness_when_greater_than_4100(self, mock_api, mock_date, mock_time):
        self.ALARM.HUE = 140
        self.ALARM.BRIGHTNESS = 10
        mock_date.datetime.now.return_value = self.MONDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 12, temp=2700, trans=4)

    def test_light_alarm_program__should_increment_hue_when_between_4000_and_4100(self, mock_api, mock_date, mock_time):
        self.ALARM.HUE = 125
        self.ALARM.BRIGHTNESS = 10
        mock_date.datetime.now.return_value = self.MONDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 255, hue=(126 * 8) + 3000, sat=250, trans=4)

    def test_light_alarm_program__should_reset_brightness_when_between_4000_and_4100(self, mock_api, mock_date, mock_time):
        self.ALARM.HUE = 125
        self.ALARM.BRIGHTNESS = 10
        mock_date.datetime.now.return_value = self.MONDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        assert self.ALARM.BRIGHTNESS == 40

    def test_light_alarm_program__should_decrement_saturation_when_between_4000_and_4100(self, mock_api, mock_date, mock_time):
        self.ALARM.HUE = 125
        self.ALARM.BRIGHTNESS = 10
        mock_date.datetime.now.return_value = self.MONDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 255, hue=(126 * 8) + 3000, sat=250, trans=4)

    def test_light_alarm_program__should_not_call_set_light_group_when_sun(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.SUNDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_alarm_program__should_not_call_set_light_group_when_wed(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.WEDNESDAY
        light_alarm_program(self.ALARM, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_on_program__should_turn_light_to_max_when_after_timer_on_matching_day(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.MONDAY + datetime.timedelta(minutes=-4)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 255)

    def test_light_on_program__should_not_turn_light_to_max_when_after_timer_on_wrong_day(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.SUNDAY
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_on_program__should_not_turn_on_light_just_before_timer(self, mock_api, mock_date, mock_time):
        before_time = self.MONDAY + datetime.timedelta(minutes=-4, seconds=-1)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = before_time
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_on_program__should_turn_on_light_when_exactly_at_timer(self, mock_api, mock_date, mock_time):
        exact_time = self.MONDAY + datetime.timedelta(minutes=-4)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = exact_time
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 255)
        assert self.LIGHT_ON.TRIGGERED is True

    def test_light_on_program__should_not_turn_on_light_after_already_turning_on(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = True
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = self.MONDAY
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_on_program__should_reset_triggered_value_after_one_minute(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = True
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        one_minute_later = self.MONDAY + datetime.timedelta(minutes=-3, seconds=1)
        mock_date.datetime.now.return_value = one_minute_later
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        assert self.LIGHT_ON.TRIGGERED is False

    def test_light_on_program__should_not_retrigger_api_call_after_one_minute(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = False
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        one_minute_later = self.MONDAY + datetime.timedelta(minutes=-3, seconds=1)
        mock_date.datetime.now.return_value = one_minute_later
        light_on_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_off_program__should_turn_light_to_min_when_after_timer_on_matching_day(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.MONDAY + datetime.timedelta(minutes=-4, seconds=30)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 0)

    def test_light_off_program__should_not_turn_light_to_min_when_before_day_timer_on_wrong_day(self, mock_api, mock_date, mock_time):
        mock_date.datetime.now.return_value = self.SUNDAY
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_off_program__should_not_turn_off_light_just_before_timer(self, mock_api, mock_date, mock_time):
        before_time = self.MONDAY + datetime.timedelta(minutes=-4, seconds=-1)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = before_time
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_off_program__should_turn_off_light_when_exactly_at_timer(self, mock_api, mock_date, mock_time):
        exact_time = self.MONDAY + datetime.timedelta(minutes=-4)
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = exact_time
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_called_with(self.API_KEY, self.GROUP_ID, 0)
        assert self.LIGHT_ON.TRIGGERED is True

    def test_light_off_program__should_not_turn_off_light_after_already_turning_off(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = True
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        mock_date.datetime.now.return_value = self.MONDAY
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()

    def test_light_off_program__should_reset_triggered_value_after_one_minute(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = True
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        one_minute_later = self.MONDAY + datetime.timedelta(minutes=-3, seconds=1)
        mock_date.datetime.now.return_value = one_minute_later
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        assert self.LIGHT_ON.TRIGGERED is False

    def test_light_off_program__should_not_retrigger_api_call_after_one_minute(self, mock_api, mock_date, mock_time):
        self.LIGHT_ON.TRIGGERED = False
        mock_date.datetime.combine.side_effect = datetime.datetime.combine
        mock_date.timedelta.side_effect = datetime.timedelta
        mock_date.date.today.return_value = datetime.datetime.today()
        one_minute_later = self.MONDAY + datetime.timedelta(minutes=-3, seconds=1)
        mock_date.datetime.now.return_value = one_minute_later
        light_off_program(self.LIGHT_ON, self.API_KEY, self.GROUP_ID)

        mock_api.assert_not_called()
