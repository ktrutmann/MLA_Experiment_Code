from ._builtin import Page
from .models import Constants


class initializer_page(Page):
    def before_next_page(self):
        self.player.initialize_round()


class condition_page(Page):
    def is_displayed(self):
        return self.player.participant.vars['i_in_block'] == 0
    # TODO: Only show if it's the first round or the condition has changed!
    # TODO: Also mention it in the instructions whether we scramble conditions or not.

    def vars_for_template(self) -> dict:
        return {'condition': self.player.participant.vars['condition']}


class trading_page(Page):
    form_model = 'player'
    form_fields = ['transaction',
                   'time_to_order',
                   'unfocused_time_to_order']

    def is_displayed(self):
        return not self.player.participant.vars['skipper']

    def vars_for_template(self):
        return self.player.get_trading_vars()


class belief_page(Page):
    form_model = 'player'
    form_fields = ['belief',
                   'time_to_belief_report',
                   'unfocused_time_to_belief_report']

    def is_displayed(self):
        return not self.player.participant.vars['skipper']

    def vars_for_template(self):
        return {'this_condition': self.player.participant.vars['condition'],
                'max_time': Constants.max_time_beliefs}

    def before_next_page(self):
        self.player.calculate_belief_bonus()


class update_page(Page):
    form_model = 'player'
    form_fields = ['update_time_used']
    timeout_seconds = Constants.update_time

    def is_displayed(self):
        return not self.player.participant.vars['skipper']

    def vars_for_template(self):
        update = self.player.participant.vars['price_path'][self.round_number] - \
            self.player.participant.vars['price_path'][self.round_number - 1]

        return {'update_raise': update >= 0,
                'update': abs(update),
                'price': self.participant.vars['price_path'][self.round_number],
                }

    def before_next_page(self):
        self.player.update_vars()


class end_page(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.calculate_final_payoff()


page_sequence = [initializer_page,
                 condition_page,
                 trading_page,
                 belief_page,
                 update_page,
                 end_page,
                 ]
