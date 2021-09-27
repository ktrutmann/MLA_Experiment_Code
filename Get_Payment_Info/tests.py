from . import *
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield payment_info_page, {'matr_nr': '42-herpaderp'}
