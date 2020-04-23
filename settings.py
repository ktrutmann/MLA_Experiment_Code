from os import environ
import dj_database_url

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.06,
    'participation_fee': 10,
    'base_bonus': 20,
    'doc': "",
    # 'use_browser_bots': True
}

SESSION_CONFIGS = [
    {
        'name': 'Investment_Task',
        'num_demo_participants': 1,
        'app_sequence': ['Investment_Task'],
        'real_world_currency_per_point': .06,
        'participation_fee': 10
    },

    {
        'name': 'Demographics',
        'num_demo_participants': 1,
        'app_sequence': ['Demographics'],
    },

    {
        'name': 'Investment_Task_Full',
        'num_demo_participants': 1,
        'app_sequence': ['Tutorial_Investment_Task', 'Investment_Task', 'Get_Payment_Info',
                         'Demographics', 'Show_Payoff'],
        'real_world_currency_per_point': .05,
        'participation_fee': 10,
        'base_bonus': 15,
        'n_probs_shown_participants': 10,
        'n_states_shown_participants': 10,
        'n_baseline_participants': 10,
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CHF'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 1

ROOM_DEFAULTS = {}
ROOMS = [
    {
        'name': 'test_room',
        'display_name': 'test_room1'
    },
    {
        'name': 'pilot_room',
        'display_name': 'pilot_room1'
    }
]

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# TODO: Change to production!
# Consider '', None, and '0' to be empty/false
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
DEBUG = True

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '$x%_exnjos2tzdh*zkh!b8v)vx0a2+j)ocjs060#9*-u6-_4##'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# Database: This is so that devserver can still be used
# DATABASES = {'default': dj_database_url.config(default='sqlite:///db.sqlite3')}

# TODO: Make it ready for the students: Write email with invitation and betatester instructions!
    # They should make screenshots and send them or write into the general comments section at the end of the study
    # They should be done till wednessday evening. The mail should be sent on monday
# TODO: Translate everything to english
# TODO: Test with other browsers!