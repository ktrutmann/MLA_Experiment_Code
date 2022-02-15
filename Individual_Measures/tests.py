from . import *
from otree.api import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield(soep_general_page, {'soep_general': 2})
        yield(soep_finance_page, {'soep_finance': 2})
        yield(soep_ambiguity_page, {'soep_ambiguity': 2})
        yield(soep_loss_aversion_page, {'soep_loss_aversion': 2})
        yield(falk_patience_page, {'falk_patience_question': 2})
        yield(chapman_impulse_page, {'chapman_impulse_question': 2})
        yield(dept_payment_page, {'prob_no_dept_payment': 33})
