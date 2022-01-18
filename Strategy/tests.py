from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield (open_strategy_page, {'strategy': 'Derp!'})
        yield (closed_strategy_page, {'strategy_random': 2, 'strategy_feeling': 2, 'strategy_rational': 2,
                                            'strategy_short_rational': 2, 'strategy_short_risk_averse': 2,
                                            'strategy_risk_averse': 2, 'strategy_inertia': 2, 'strategy_DE': 2,
                                            'strategy_anti_DE': 2})
