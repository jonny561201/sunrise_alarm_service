from svc.utilities.api_utils import get_light_groups


def update_light_groups(api_key, group_id, on):
    if group_id.upper() == 'ALL':
        get_light_groups(api_key)