from svc.utilities import api_utils


def update_light_groups(api_key, group_id, on, brightness=None):
    if group_id.upper() == 'ALL':
        groups = api_utils.get_light_groups(api_key)
        group_ids = [group_id for group_id, data in groups.items()]
        for g_id in group_ids:
            api_utils.set_light_groups(api_key, g_id, on, __calculate_brightness(on, brightness))
    else:
        api_utils.set_light_groups(api_key, group_id, on, __calculate_brightness(on, brightness))


def __calculate_brightness(on, brightness):
    if not on:
        return 0
    return 255 if brightness is None else brightness
