import datetime


class ThreadState:
    ACTIVE_THREAD = None
    THREAD_ID = None


class LightAlarmState(ThreadState):
    HUE = 0
    BRIGHTNESS = 0
    SATURATION = 255
    ALARM_START_TIME = None
    ALARM_STOP_TIME = None
    ALARM_DAYS = None

    def __init__(self, task_id: str, alarm_time: datetime.time, alarm_days: str):
        self.THREAD_ID = task_id
        self.ALARM_DAYS = alarm_days
        eight_minutes_prior = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=-8)).time()
        two_minutes_after = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=+2)).time()
        self.ALARM_START_TIME = eight_minutes_prior
        self.ALARM_STOP_TIME = two_minutes_after


class LightOnOffState(ThreadState):
    TRIGGERED = False
    ALARM_START_TIME = None
    ALARM_DAYS = None

    def __init__(self, task_id: str, alarm_time: datetime.time, alarm_days: str):
        self.THREAD_ID = task_id
        self.ALARM_DAYS = alarm_days
        self.ALARM_START_TIME = datetime.datetime.combine(datetime.date.today(), alarm_time).time()
