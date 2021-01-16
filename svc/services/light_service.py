from svc.constants.lights_state import LightState
from svc.constants.settings_state import Settings
from svc.utilities.api_utils import get_light_tasks_by_user


# TODO: how should I get the devices default user id....would be easier if the database was cloud based...
# TODO: pass the task_id field to the add replace function
# TODO: update the add replace function to use the task id to determine when a task needs to be replaced
def create_light_alarm():
    user_id = Settings.get_instance().user_id
    light_tasks = get_light_tasks_by_user(user_id)
    for task in light_tasks:
        if task['alarm_time'] is not None and task['alarm_days'] is not None and task['alarm_light_group'] is not None:
            LightState.get_instance().add_light_alarm(task['task_id'], task['alarm_light_group'], task['alarm_time'], task['alarm_days'])
