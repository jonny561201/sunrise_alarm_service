import logging

from svc.constants.home_automation import Automation
from svc.constants.thread_state import ThreadState
from svc.services.light_service import create_light_alarm
from svc.utilities.event_utils import create_thread

logging.basicConfig(filename='sunriseAlarm.log', level=logging.INFO)

try:
    logging.info('Application started!')
    create_light_alarm()
    create_thread(ThreadState(), create_light_alarm, Automation.TIME.ONE_MINUTE)
except Exception:
    logging.error('Application interrupted by user')
