from . import *
from otree.api import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield(soep_general_page, {'soep_general': 2})
        yield(soep_driving_page, {'soep_driving': 2})
        yield(soep_finance_page, {'soep_finance': 2})
        yield(soep_leisure_page, {'soep_leisure': 2})
        yield(soep_occupation_page, {'soep_occupation': 2})
        yield(soep_health_page, {'soep_health': 2})
        yield(soep_faith_in_people_page, {'soep_faith_in_people': 2})
