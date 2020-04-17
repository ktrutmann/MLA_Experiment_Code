from otree.api import Currency as c, currency_range
from ._builtin import Page


class payoff_page(Page):
    def vars_for_template(self):
        return self.participant.vars['payoff_dict']

page_sequence = [payoff_page]
