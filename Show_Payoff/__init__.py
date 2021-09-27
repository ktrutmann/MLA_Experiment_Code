from otree.api import *


author = 'Kevin Trutmann'
doc = """
Showing what participants have earned in which block.
"""


class Constants(BaseConstants):
    name_in_url = 'show_payoff'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES
class payoff_page(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return player.participant.vars['payoff_dict']


page_sequence = [payoff_page]
