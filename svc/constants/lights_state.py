from svc.constants.home_automation import Automation
from svc.constants.settings_state import Settings
from svc.constants.thread_state import LightAlarmState, LightOnOffState
from svc.utilities.api_utils import get_light_api_key
from svc.utilities.event_utils import create_thread
from svc.utilities.light_utils import light_alarm_program, light_on_program, light_off_program


class LightState:
    __instance = None
    API_KEY = None
    LIGHT_ALARMS = []

    def __init__(self):
        if LightState.__instance is not None:
            raise Exception
        else:
            LightState.__instance = self

    def add_light_alarm(self, task):
        task_id = task['task_id']
        task_type = task['task_type']
        if not any(alarm.THREAD_ID == task_id for alarm in self.LIGHT_ALARMS):
            light_group_id = task['alarm_light_group']
            if task_type == Automation.LIGHT.SUNRISE:
                alarm = LightAlarmState(task_id, task['alarm_time'], task['alarm_days'])
                alarm.ACTIVE_THREAD = create_thread(lambda: light_alarm_program(alarm, self.get_light_api_key(), light_group_id), Automation.TIME.TWO_SECONDS)
                alarm.ACTIVE_THREAD.start()
                self.LIGHT_ALARMS.append(alarm)
            elif task_type == Automation.LIGHT.TURN_ON:
                alarm = LightOnOffState(task_id, task['alarm_time'], task['alarm_days'])
                alarm.ACTIVE_THREAD = create_thread(lambda: light_on_program(alarm, self.get_light_api_key(), light_group_id), Automation.TIME.TEN_SECONDS)
                alarm.ACTIVE_THREAD.start()
                self.LIGHT_ALARMS.append(alarm)
            elif task_type == Automation.LIGHT.TURN_OFF:
                alarm = LightOnOffState(task_id, task['alarm_time'], task['alarm_days'])
                alarm.ACTIVE_THREAD = create_thread(lambda: light_off_program(alarm, self.get_light_api_key(), light_group_id), Automation.TIME.TEN_SECONDS)
                alarm.ACTIVE_THREAD.start()
                self.LIGHT_ALARMS.append(alarm)

    def remove_light_alarm(self, task_id):
        index = next((i for i, x in enumerate(self.LIGHT_ALARMS) if x.THREAD_ID == task_id), None)
        if index is not None:
            existing_alarm = self.LIGHT_ALARMS.pop(index)
            existing_alarm.ACTIVE_THREAD.stopped.set()

    def get_light_api_key(self):
        if self.API_KEY is None:
            settings = Settings.get_instance()
            self.API_KEY = get_light_api_key(settings.light_api_user, settings.light_api_password)
        return self.API_KEY

    @staticmethod
    def get_instance():
        if LightState.__instance is None:
            LightState.__instance = LightState()
        return LightState.__instance
