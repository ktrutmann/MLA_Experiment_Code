from . import pages
from ._builtin import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield pages.payment_info_page, {'matr_nr': '42-herpaderp'}
