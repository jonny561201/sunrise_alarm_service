import logging

from svc.constants.home_automation import Automation
from svc.constants.settings_state import Settings
from svc.constants.thread_state import LightAlarmState
from svc.utilities.api_utils import get_light_api_key
from svc.utilities.event_utils import create_thread
from svc.utilities.light_utils import run_light_program


class LightState:
    __instance = None
    API_KEY = None
    LIGHT_ALARMS = []

    def __init__(self):
        if LightState.__instance is not None:
            raise Exception
        else:
            LightState.__instance = self

    def add_light_alarm(self, task_id, light_group_id, alarm_time, alarm_days):
        if not any(alarm.THREAD_ID == task_id for alarm in self.LIGHT_ALARMS):
            logging.info(f'-----added new light alarm id: {task_id}-----')
            alarm = LightAlarmState(task_id, light_group_id, alarm_time, alarm_days)
            alarm.ACTIVE_THREAD = create_thread(lambda: run_light_program(alarm, self.get_light_api_key(), light_group_id), Automation.TIME.TEN_SECONDS)
            alarm.ACTIVE_THREAD.start()
            self.LIGHT_ALARMS.append(alarm)

    def remove_light_alarm(self, task_id):
        index = next((i for i, x in enumerate(self.LIGHT_ALARMS) if x.THREAD_ID == task_id), None)
        if index is not None:
            logging.info(f'-----removed light alarm id: {task_id}-----')
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
