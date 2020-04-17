from ._builtin import Page, WaitPage
from .models import Constants


class initializer_page(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # Put them into the different conditions:
        if self.player.id_in_group <= self.session.config['n_probs_shown_participants']:
            self.player.participant.vars['main_condition'] = 'probs_shown'
        elif self.player.id_in_group <=\
                self.session.config['n_probs_shown_participants'] +\
                self.session.config['n_states_shown_participants']:
            self.player.participant.vars['main_condition'] = 'states_shown'
        else:
            self.player.participant.vars['main_condition'] = 'baseline'

        # self.participant.vars['belief_elicitation'] = self.participant.vars['main_condition'] != 'baseline'
        self.participant.vars['belief_elicitation'] = True  # Belief elicitation everywhere


class tutorial_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_tutorial_vars()

    def before_next_page(self):
        self.player.make_price_paths()
        self.player.initialize_portfolio()


class trading_page(Page):
    form_model = 'player'
    form_fields = ['transaction']

    def vars_for_template(self):
        return self.player.get_trading_vars()


class belief_page(Page):
    form_model = 'player'
    form_fields = ['belief']

    def is_displayed(self) -> bool:
        return self.participant.vars['belief_elicitation']

    def vars_for_template(self) -> dict:
        return {'max_time': Constants.max_time_beliefs}


class updating_page(Page):
    timeout_seconds = Constants.update_time

    def vars_for_template(self):
        update = self.player.participant.vars['price_path'][self.round_number] - \
            self.player.participant.vars['price_path'][self.round_number - 1]

        return {'update_raise': update >= 0,
                'update': abs(update),
                'price': self.player.participant.vars['price_path'][self.round_number]
                }

    def before_next_page(self):
        if self.round_number < Constants.num_rounds:
            self.player.update_vars()


class quiz_page(Page):
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6',
                   'wrong_answers']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return self.player.get_tutorial_vars()


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
                 quiz_page,
                 end_page]
