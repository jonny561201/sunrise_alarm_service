import datetime


class ThreadState:
    ACTIVE_THREAD = None
    STOP_EVENT = None


class LightAlarmState(ThreadState):
    ALARM_COUNTER = 0
    ALARM_START_TIME = None
    ALARM_STOP_TIME = None
    ALARM_DAYS = None
    LIGHT_GROUP_ID = None

    def __init__(self, light_group_id, alarm_time, alarm_days):
        self.LIGHT_GROUP_ID = light_group_id
        self.ALARM_DAYS = alarm_days
        self.ALARM_START_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=-10)).time()
        self.ALARM_STOP_TIME = (datetime.datetime.combine(datetime.date.today(), alarm_time) + datetime.timedelta(minutes=+10)).time()
