import logging

from svc.services.light_service import create_light_alarm

logging.basicConfig(filename='sunriseAlarm.log', level=logging.DEBUG)

try:
    logging.info('Application started!')
    create_light_alarm()
except Exception:
    logging.error('Application interrupted by user')
