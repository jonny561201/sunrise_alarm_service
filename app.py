import logging

from svc.constants.home_automation import Automation
from svc.services.light_service import create_light_alarm
from svc.utilities.event_utils import create_thread

logging.basicConfig(filename='sunriseAlarm.log', level=logging.INFO)

try:
    logging.info('Application started!')
    thread = create_thread(create_light_alarm, Automation.TIME.ONE_MINUTE)
    thread.start()
except Exception:
    logging.error('Application interrupted by user')
