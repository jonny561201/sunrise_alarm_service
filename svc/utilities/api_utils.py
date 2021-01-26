import base64
import logging
from datetime import time
import json

import requests

from svc.constants.home_automation import Automation
from svc.constants.settings_state import Settings


def get_light_api_key(username, password):
    body = {'devicetype': Automation().APP_NAME}
    auth = base64.b64encode((username + ':' + password).encode('UTF-8')).decode('UTF-8')
    headers = {'Authorization': 'Basic ' + auth}
    try:
        response = requests.post(Settings.get_instance().light_base_url, data=json.dumps(body), headers=headers, timeout=5)
        api_key = response.json()[0]['success']['username']
        return api_key
    except Exception:
        return None


# TODO: try catch for errors!!!
def set_light_groups(api_key, group_id, state, brightness=None):
    url = Settings.get_instance().light_base_url + '/%s/groups/%s/action' % (api_key, group_id)
    request = {'on': state}
    if brightness is not None:
        request['on'] = True
        request['bri'] = brightness
    try:
        requests.put(url, data=json.dumps(request))
    except Exception:
        logging.error('Set Light Groups Put request threw an exception')


def get_light_tasks_by_user(user_id):
    base_url = Settings.get_instance().hub_base_url
    try:
        response = requests.get(f'{base_url}/userId/{user_id}/tasks', timeout=5)
        light_response = response.json()
        for task in light_response:
            task['alarm_time'] = None if task.get('alarm_time') is None else time.fromisoformat(task['alarm_time'])
        return light_response
    except Exception:
        return []
