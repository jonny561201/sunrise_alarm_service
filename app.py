import logging


logging.basicConfig(filename='sunriseAlarm.log', level=logging.DEBUG)

try:
    logging.info('Application started!')
except Exception:
    logging.error('Application interrupted by user')
