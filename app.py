import logging


logging.basicConfig(filename='sunriseAlarm.log', level=logging.DEBUG)

try:
    logging.info('Application started!')
except KeyboardInterrupt:
    logging.error('Application interrupted by user')
