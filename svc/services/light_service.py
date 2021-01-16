from svc.constants.lights_state import LightState
from svc.constants.settings_state import Settings
from svc.utilities.api_utils import get_light_tasks_by_user


# TODO: how should I get the devices default user id....would be easier if the database was cloud based...
def create_light_alarm():
    light_state = LightState.get_instance()
    user_id = Settings.get_instance().user_id
    light_tasks = get_light_tasks_by_user(user_id)
    __add_new_alarms(light_state, light_tasks)
    __remove_cancelled_alarms(light_state, light_tasks)


def __add_new_alarms(light_state, light_tasks):
    for task in light_tasks:
        if task['alarm_time'] is not None and task['alarm_days'] is not None and task['alarm_light_group'] is not None:
            light_state.add_light_alarm(task['task_id'], task['alarm_light_group'], task['alarm_time'],
                                        task['alarm_days'])


def __remove_cancelled_alarms(light_state, light_tasks):
    alarm_ids = {alarm.THREAD_ID for alarm in light_state.LIGHT_ALARMS}
    request_ids = {task['task_id'] for task in light_tasks}
    missing_items = alarm_ids - request_ids
    for item in missing_items:
        light_state.remove_light_alarm(item)

