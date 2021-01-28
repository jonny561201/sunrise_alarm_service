import datetime

from svc.utilities.api_utils import set_light_groups


# TODO: check to see if light is currently on before trying to turn on???
def light_alarm_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    day_name = now.strftime('%a')
    if __is_within_alarm(alarm_state, day_name, now):
        alarm_state.ALARM_COUNTER += 2
        set_light_groups(api_key, group_id, True, alarm_state.ALARM_COUNTER)
    elif alarm_state.ALARM_COUNTER != 0:
        alarm_state.ALARM_COUNTER = 0


def __is_within_alarm(light_state, day_name, now):
    return day_name in light_state.ALARM_DAYS \
           and light_state.ALARM_START_TIME <= now.time() < light_state.ALARM_STOP_TIME \
           and light_state.ALARM_COUNTER <= 254


def light_on_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    one_minute_after = (datetime.datetime.combine(datetime.date.today(), alarm_state.ALARM_START_TIME) + datetime.timedelta(minutes=1)).time()
    current_time = now.time()
    if __is_within_on_time(now.strftime('%a'), alarm_state, current_time, one_minute_after):
        set_light_groups(api_key, group_id, True, 255)
        alarm_state.TRIGGERED = True
    if alarm_state.TRIGGERED and current_time > one_minute_after:
        alarm_state.TRIGGERED = False


def light_off_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    current_time = now.time()
    one_minute_after = (datetime.datetime.combine(datetime.date.today(), alarm_state.ALARM_START_TIME) + datetime.timedelta(minutes=1)).time()
    if __is_within_on_time(now.strftime('%a'), alarm_state, current_time, one_minute_after):
        set_light_groups(api_key, group_id, False, 0)
        alarm_state.TRIGGERED = True
    if alarm_state.TRIGGERED and current_time > one_minute_after:
        alarm_state.TRIGGERED = False


def __is_within_on_time(day_name, alarm_state, current_time, one_minute_after):
    return day_name in alarm_state.ALARM_DAYS \
           and current_time >= alarm_state.ALARM_START_TIME \
           and not alarm_state.TRIGGERED \
           and current_time < one_minute_after
