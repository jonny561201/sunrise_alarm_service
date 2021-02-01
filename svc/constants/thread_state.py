import datetime


class ThreadState:
    ACTIVE_THREAD = None
    THREAD_ID = None


class LightAlarmState(ThreadState):
    ALARM_COUNTER = 0
    ALARM_START_TIME = None
    ALARM_STOP_TIME = None
    ALARM_DAYS = None

    def __init__(self, task_id: str, alarm_time: datetime.time, alarm_days: str):
        self.THREAD_ID = task_id
        self.ALARM_DAYS = alarm_days
        self.ALARM_START_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=-25)).time()
        self.ALARM_STOP_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=+5)).time()


class LightOnOffState(ThreadState):
    TRIGGERED = False
    ALARM_START_TIME = None
    ALARM_DAYS = None

    def __init__(self, task_id: str, alarm_time: datetime.time, alarm_days: str):
        self.THREAD_ID = task_id
        self.ALARM_DAYS = alarm_days
        self.ALARM_START_TIME = datetime.datetime.combine(datetime.date.today(), alarm_time).time()
