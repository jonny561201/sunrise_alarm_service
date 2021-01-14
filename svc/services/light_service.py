from svc.constants.lights_state import LightState
from svc.constants.settings_state import Settings
from svc.utilities.api_utils import get_light_preferences_by_user


# TODO: how should I get the devices default user id....would be easier if the database was cloud based...
def create_light_alarm():
    user_id = Settings.get_instance().user_id
    light_pref = get_light_preferences_by_user(user_id)
    if light_pref['alarm_time'] is not None and light_pref['alarm_days'] is not None and light_pref['alarm_light_group'] is not None:
        LightState.get_instance().add_replace_light_alarm(light_pref['alarm_light_group'], light_pref['alarm_time'], light_pref['alarm_days'])
