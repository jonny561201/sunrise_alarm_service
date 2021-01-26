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
    day_name = now.strftime('%a')
    if day_name in alarm_state.ALARM_DAYS and now.time() >= alarm_state.ALARM_START_TIME:
        set_light_groups(api_key, group_id, True, 0)
