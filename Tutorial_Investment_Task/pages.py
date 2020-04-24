from ._builtin import Page, WaitPage
from .models import Constants


class initializer_page(Page):
    pass
    # def before_next_page(self):
    #     self.player.initialize_round()


class tutorial_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_tutorial_vars()


class trading_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    def vars_for_template(self):
        return self.player.get_trading_vars()


class belief_page(Page):
    form_model = 'player'
    form_fields = ['belief']

    def vars_for_template(self):
        return {'max_time': Constants.max_time_beliefs}


class updating_page(Page):
    timeout_seconds = Constants.update_time

    def vars_for_template(self):
        update = self.player.participant.vars['price_info'].price[self.round_number] - \
            self.player.participant.vars['price_info'].price[self.round_number - 1]

        return {'update_raise': update >= 0,
                'update': abs(update),
                'new_price': self.participant.vars['price_info'].price[self.round_number]
                }

# TODO (after pilot): Bring back the quizz!
# class quiz_page(Page):
#     form_model = 'player'
#     form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6',
#                    'wrong_answers']
#
#     def is_displayed(self):
#         return self.round_number == Constants.num_rounds
#
#     def vars_for_template(self):
#         return self.player.get_tutorial_vars()


class end_page(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return self.player.get_trading_vars()


page_sequence = [initializer_page,
                 tutorial_page,
                 trading_page,
                 belief_page,
                 updating_page,
                 # quiz_page,
                 end_page]
