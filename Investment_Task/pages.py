from ._builtin import Page, WaitPage
from .models import Constants


class initializer_page(Page):
    def before_next_page(self):
        if self.round_number == 1:
            # If we are playing in "standalone mode", set the main condition here.
            if 'main_condition' not in self.participant.vars.keys():
                self.participant.vars['main_condition'] = 'probs_shown'
                self.participant.vars['belief_elicitation'] = True

            #Set the condition sequence:
            self.participant.vars['condition_sequence'] = [self.participant.vars['main_condition']
                                                           if this_condition == 'main_condition' else this_condition
                                                           for this_condition in Constants.condition_sequence]
            self.player.make_price_paths(conditions=self.participant.vars['condition_sequence'],
                                         save_path=False)

            self.player.participant.vars['i_in_block'] = 0
            self.player.participant.vars['i_block'] = 0
            self.player.participant.vars['condition'] = self.participant.vars['condition_sequence'][0]
            self.player.participant.vars['skipper'] = False  # To skip the last round of a block (for the price path)

            self.player.calculate_bayesian_prob()
        else:
            self.player.advance_round()

        if self.player.participant.vars['i_in_block'] == 0:
            self.player.initialize_portfolio()


class condition_page(Page):
    def is_displayed(self):
        return self.player.participant.vars['i_in_block'] == 0

    def vars_for_template(self) -> dict:
        return {'condition': self.player.participant.vars['condition']}


class trading_page(Page):
    form_model = 'player'
    form_fields = ['transaction',
                   'time_to_order',
                   'unfocused_time_to_order']

    def vars_for_template(self):
        return self.player.get_trading_vars()

    def is_displayed(self):
        return not self.player.participant.vars['skipper']


class belief_page(Page):
    form_model = 'player'
    form_fields = ['belief',
                   'time_to_belief_report',
                   'unfocused_time_to_belief_report']

    def is_displayed(self):
        return self.player.participant.vars['belief_elicitation'] and not self.player.participant.vars['skipper']

    def vars_for_template(self):
        state_srt = 'schlechten'
        raise_prob = 1 - Constants.up_prob
        if self.player.participant.vars['good_state'][self.round_number - 1]:
            state_srt = 'guten'
            raise_prob = Constants.up_prob

        return {'this_condition': self.player.participant.vars['condition'],
                'bayes_prob': round(self.player.participant.vars['bayes_prob_up'][self.round_number - 1] * 100, 2),
                'state_str': state_srt,
                'obj_prob': round(raise_prob * 100, 2),
                'max_time': Constants.max_time_beliefs}

    def before_next_page(self):
        self.player.calculate_belief_bonus()


class update_page(Page):
    timeout_seconds = Constants.update_time
    form_model = 'player'
    form_fields = ['update_time_used']

    def vars_for_template(self):
        update = self.player.participant.vars['price_path'][self.round_number] - \
            self.player.participant.vars['price_path'][self.round_number - 1]

        return {'update_raise': update >= 0,
                'update': abs(update),
                'price': self.participant.vars['price_path'][self.round_number],
                }

    def before_next_page(self):
        self.player.update_vars()

    def is_displayed(self):
        return not self.player.participant.vars['skipper']


class end_page(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        blockend_rounds = list(range(Constants.n_periods_per_block, Constants.num_rounds + 1,
                                     Constants.n_periods_per_block + 1))
        end_cash_list = [self.player.in_round(i).final_cash - Constants.starting_cash for i in blockend_rounds]
        sum_end_cash = sum(end_cash_list)

        end_belief_bonus_list = [self.player.in_round(i).belief_bonus_cumulative for i in blockend_rounds]
        sum_end_belief_bonus = sum(end_belief_bonus_list)

        # Add the base_payoff to the game-payoff and make sure that it is floored at 0
        self.player.payoff = self.session.config['base_bonus'] *\
            (1 / self.session.config['real_world_currency_per_point'])

        if self.participant.payoff < 0:
            self.participant.payoff -= self.participant.payoff  # For some reason 0 didn't work.

        self.player.participant.vars['payoff_dict'] = {'payoff_list': zip(end_cash_list, end_belief_bonus_list),
                                               'end_cash_sum': sum_end_cash,
                                               'belief_bonus_sum': sum_end_belief_bonus,
                                               'payoff_game': sum_end_cash + sum_end_belief_bonus,
                                               'payoff_total': self.participant.payoff_plus_participation_fee(),
                                               'showup_fee': self.session.config['participation_fee'],
                                               'base_payoff': self.session.config['base_bonus'],
                                               'percent_conversion':
                                                       self.session.config['real_world_currency_per_point'] * 100
                                                       }


page_sequence = [initializer_page,
                 condition_page,
                 trading_page,
                 belief_page,
                 update_page,
                 end_page,
                 ]
