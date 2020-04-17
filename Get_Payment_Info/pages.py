from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class payment_info_page(Page):
    form_model = 'player'
    form_fields = ['booth_nr']

    def before_next_page(self):
        # Create or increase the queue-number
        if 'queue_nr' in self.session.vars:
            self.session.vars['queue_nr'] += 1
        else:
            self.session.vars['queue_nr'] = 1

        self.player.participant.label = '{} (booth {})'.format(
            self.session.vars['queue_nr'], self.player.booth_nr)

        self.player.participant.vars['payoff_dict']['queue_nr'] = self.session.vars['queue_nr']


page_sequence = [
    payment_info_page,
]
