import datetime
import logging
import time

from svc.utilities.api_utils import set_light_groups


# TODO: check to see if light is currently on before trying to turn on???
def light_alarm_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    day_name = now.strftime('%a')
    within_alarm = __is_within_alarm(alarm_state, day_name, now)
    if within_alarm:
        alarm_state.HUE += 1
        hue = (alarm_state.HUE * 8) + 3000
        if 4100 > hue > 4000:
            set_light_groups(api_key, group_id, 255, hue=hue, sat=alarm_state.SATURATION)
            alarm_state.SATURATION -= 5
            alarm_state.BRIGHTNESS = 40
        elif hue >= 4100:
            alarm_state.BRIGHTNESS += 2
            set_light_groups(api_key, group_id, alarm_state.BRIGHTNESS, temp=2700, trans=0)
        else:
            alarm_state.BRIGHTNESS += 1
            update_bri = alarm_state.BRIGHTNESS * 4
            set_light_groups(api_key, group_id, update_bri if update_bri < 255 else 255, hue=hue, sat=alarm_state.SATURATION)
    elif not within_alarm and alarm_state.BRIGHTNESS != 0:
        alarm_state.HUE = 0
        alarm_state.BRIGHTNESS = 0
        alarm_state.SATURATION = 255


def __is_within_alarm(light_state, day_name, now):
    return day_name in light_state.ALARM_DAYS \
           and light_state.ALARM_START_TIME <= now.time() < light_state.ALARM_STOP_TIME


def light_on_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    one_minute_after = (datetime.datetime.combine(datetime.date.today(), alarm_state.ALARM_START_TIME) + datetime.timedelta(minutes=1)).time()
    current_time = now.time()
    if __is_within_on_time(now.strftime('%a'), alarm_state, current_time, one_minute_after):
        logging.info(f'Api call to Turn on: {group_id} at {current_time} for Task Id: {alarm_state.THREAD_ID}')
        set_light_groups(api_key, group_id, True, 255)
        time.sleep(1)
        set_light_groups(api_key, group_id, 255)
        alarm_state.TRIGGERED = True
    if alarm_state.TRIGGERED and current_time > one_minute_after:
        alarm_state.TRIGGERED = False


def light_off_program(alarm_state, api_key, group_id):
    now = datetime.datetime.now()
    current_time = now.time()
    one_minute_after = (datetime.datetime.combine(datetime.date.today(), alarm_state.ALARM_START_TIME) + datetime.timedelta(minutes=1)).time()
    if __is_within_on_time(now.strftime('%a'), alarm_state, current_time, one_minute_after):
        logging.info(f'Api call to Turn off: {group_id} at {current_time} for Task Id: {alarm_state.THREAD_ID}')
        set_light_groups(api_key, group_id, 0)
        time.sleep(1)
        set_light_groups(api_key, group_id, 0)
        alarm_state.TRIGGERED = True
    if alarm_state.TRIGGERED and current_time > one_minute_after:
        alarm_state.TRIGGERED = False


def __is_within_on_time(day_name, alarm_state, current_time, one_minute_after):
    return day_name in alarm_state.ALARM_DAYS \
           and current_time >= alarm_state.ALARM_START_TIME \
           and not alarm_state.TRIGGERED \
           and current_time < one_minute_after
