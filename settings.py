from os import environ


SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.02,
    'participation_fee': 6.65,
    'base_bonus': 1.5,
    'doc': "",
}
# TODO: (1) Recalculate payoff using pre-pilot. 6.5 + 1.5 base bonus + max .6 ravens. Max 1.5. winnings in task
# TODO: (2) Programm tests for everything

SESSION_CONFIGS = [
    {
        'name': 'Investment_Task',
        'num_demo_participants': 1,
        'app_sequence': ['Investment_Task'],
    },
 
    {
        'name': 'Investment_Task_Full',
        'num_demo_participants': 1,
        'app_sequence': [#'Tutorial_Investment_Task',
            'Investment_Task',
                         'Strategy', 'SOEP_Risk', # TODO: (3) Add an impulsiveness question? See sinergia.
                         'Ravens_Matrices', 'Demographics', 'Show_Payoff']
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
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

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '$x%_exnjos2tzdh*zkh!b8v)vx0a2+j)ocjs060#9*-u6-_4##'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

