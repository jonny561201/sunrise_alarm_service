import base64
import json

import requests

from svc.constants.home_automation import Automation

LIGHT_BASE_URL = 'http://192.168.1.142:80/api'


def get_light_api_key(username, password):
    body = {'devicetype': Automation().APP_NAME}
    auth = base64.b64encode((username + ':' + password).encode('UTF-8')).decode('UTF-8')
    headers = {'Authorization': 'Basic ' + auth}
    try:
        response = requests.post(LIGHT_BASE_URL, data=json.dumps(body), headers=headers, timeout=5)
        api_key = response.json()[0]['success']['username']
        return api_key
    except Exception:
        return None


def set_light_groups(api_key, group_id, state, brightness=None):
    url = LIGHT_BASE_URL + '/%s/groups/%s/action' % (api_key, group_id)
    request = {'on': state}
    if brightness is not None:
        request['on'] = True
        request['bri'] = brightness

    requests.put(url, data=json.dumps(request))


def get_preferences_by_user(user_id):
    pass
