from otree.api import Submission
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            # yield Submission(pages.initializer_page, check_html=False)
            yield Submission(pages.tutorial_page, {'transaction': 1}, check_html=False)

        # yield Submission(pages.trading_page, {'transaction': 0}, check_html=False)
        # yield Submission(pages.belief_page, {'belief': 5}, check_html=False)
        # yield (pages.updating_page)
        #
        if self.round_number == Constants.num_rounds:
            # yield Submission(pages.quiz_page,
            #                  {'Q1': '...gleich gross wie die Wahrscheinlichkeit, dass er um 5 sinkt.',
            #                   'Q2': '...wahrscheinlicher im schlechten als im guten Zustand.',
            #                   'Q3': '...ist es wahrscheinlicher, dass Sie im guten Zustand bleibt.',
            #                   'Q4': 'Ich gehe automatisch die Wette ein und erhalte die Bonuspunkte falls ' +
            #                         'der Preis nun ansteigt.',
            #                   'Q5': 'Wenn ich mir relativ sicher bin, dass der Preis der Aktie steigen wird.',
            #                   'Q6': '2010',
            #                   'wrong_answers': 2},
            #                  check_html=False)
            yield pages.end_page
