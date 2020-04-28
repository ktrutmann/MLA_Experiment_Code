from ._builtin import Page
from .models import Constants


class initializer_page(Page):
    def before_next_page(self):
        self.player.initialize_round()


class condition_page(Page):
    def is_displayed(self):
        return self.player.i_round_in_path == 0

    def vars_for_template(self):
        return {'condition': self.player.condition_name,
                'drift_list': [round(i * 100) for i in Constants.up_probs],
                'periods_per_phase': Constants.n_periods_per_phase,
                'exp_email': Constants.experimenter_email}


class trading_page(Page):
    form_model = 'player'
    form_fields = ['transaction',
                   'time_to_order',
                   'unfocused_time_to_order',
                   'changed_mind',
                   'erroneous_trade'
                   ]

    def is_displayed(self):
        return self.player.should_display_infos()

    def vars_for_template(self):
        return self.player.get_trading_vars()


class belief_page(Page):  # TODO (After Pilot): Rethink when to ask for beliefs
    form_model = 'player'
    form_fields = ['belief',
                   'time_to_belief_report',
                   'unfocused_time_to_belief_report']

    def is_displayed(self):
        return self.player.should_display_infos()

    def vars_for_template(self):
        return {'max_time': Constants.max_time_beliefs}

    def before_next_page(self):
        self.player.calculate_belief_bonus()


class update_page(Page):
    form_model = 'player'
    form_fields = ['update_time_used']
    timeout_seconds = Constants.update_time

    def is_displayed(self):
        return self.player.should_display_infos()

    def vars_for_template(self):
        return {'update_list': self.player.make_update_list()}


class end_page(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        print('Calling before_next_page of the end_page!')
        self.player.calculate_final_payoff()


page_sequence = [initializer_page,
                 condition_page,
                 trading_page,
                 belief_page,
                 update_page,
                 end_page,
                 ]
