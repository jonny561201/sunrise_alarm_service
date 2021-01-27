from svc.utilities import api_utils


def update_light_groups(api_key, group_id, on):
    if group_id.upper() == 'ALL':
        groups = api_utils.get_light_groups(api_key)
        group_ids = [group_id for group_id, data in groups.items()]
        for id in group_ids:
            api_utils.set_light_groups(api_key, id, on, 255)