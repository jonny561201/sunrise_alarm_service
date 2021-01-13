import os

from svc.constants.settings_state import Settings


class TestState:
    SETTINGS = None
    USER_ID = 'sdf234'
    DB_PORT = '5231'
    DB_USER = 'test_user'
    DB_PASS = 'test_pass'
    DB_NAME = 'fake_name'
    EMAIL_APP_ID = 'abc123'
    WEATHER_APP_ID = '345def'
    JWT_SECRET = 'FakeSecret'
    LIGHT_API_USER = 'lightUser'
    LIGHT_API_PASSWORD = 'lightPass'

    def setup_method(self):
        os.environ.update({'LIGHT_API_USERNAME': self.LIGHT_API_USER,
                           'LIGHT_API_PASSWORD': self.LIGHT_API_PASSWORD,
                           'USER_ID': self.USER_ID})
        self.SETTINGS = Settings.get_instance()

    def teardown_method(self):
        os.environ.pop('USER_ID')
        os.environ.pop('LIGHT_API_USERNAME')
        os.environ.pop('LIGHT_API_PASSWORD')

    def test_light_api_user__should_return_env_var_value(self):
        assert self.SETTINGS.light_api_user == self.LIGHT_API_USER

    def test_light_api_password__should_return_env_var_value(self):
        assert self.SETTINGS.light_api_password == self.LIGHT_API_PASSWORD

    def test_user_id__should_return_env_var_value(self):
        assert self.SETTINGS.user_id == self.USER_ID

    def test_light_api_user__should_pull_from_dictionary_if_dev_mode(self):
        light_api_user = 'other_light_user'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'LightApiUser': light_api_user}
        assert self.SETTINGS.light_api_user == light_api_user

    def test_light_api_password__should_pull_from_dictionary_if_dev_mode(self):
        light_api_password = 'other_light_password'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'LightApiPass': light_api_password}
        assert self.SETTINGS.light_api_password == light_api_password

    def test_user_id__should_pull_from_dictionary_if_dev_mode(self):
        user_id = 'other_user_id'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'UserId': user_id}
        assert self.SETTINGS.user_id == user_id
