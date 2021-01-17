import datetime


class ThreadState:
    ACTIVE_THREAD = None
    THREAD_ID = None


class LightAlarmState(ThreadState):
    ALARM_COUNTER = 0
    ALARM_START_TIME = None
    ALARM_STOP_TIME = None
    ALARM_DAYS = None
    LIGHT_GROUP_ID = None

    def __init__(self, task_id: str, light_group_id: str, alarm_time: datetime.time, alarm_days: str):
        self.THREAD_ID = task_id
        self.ALARM_DAYS = alarm_days
        self.LIGHT_GROUP_ID = light_group_id
        self.ALARM_START_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=-10)).time()
        self.ALARM_STOP_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=+10)).time()
