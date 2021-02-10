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


def set_light_groups(api_key, group_id, brightness, hue=None, temp=None, sat=255, trans=0):
    url = f'{Settings.get_instance().light_base_url}/{api_key}/groups/{group_id}/action'
    request = {'on': False if brightness == 0 else True, 'transitiontime': trans}
    if brightness != 0:
        request['bri'] = brightness
    if hue is not None:
        request['hue'] = hue
        request['sat'] = sat
    if temp is not None:
        request['ct'] = temp
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
        return None
