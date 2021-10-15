import copy
import random as rd
import string

import pandas as pd
from otree.api import *


author = 'Kevin Trutmann'
doc = """
    This is the main investment task app. See the Readme.md for more information.
"""


class Constants(BaseConstants):
    name_in_url = 'Investment_Task'
    players_per_group = None
    # Experimental Flow
    n_periods_per_phase = 4  # How long should the participants be "blocked"?
    n_distinct_paths = 7  # How many paths should be generated?
    condition_names = [
        'full_control',
        'blocked_full_info',
        'blocked_blocked_info',
    ]  # List of the conditions
    n_phases = 2  # How many phases should there be per condition
    hold_range = [-4, 4]  # What's the minimum and maximum amount of shares that can be held.
    shuffle_conditions = True  # Should the conditions be presented in "blocks" or shuffled?
    scramble_moves_in_phases = False  # Should price moves within phases be scrambled between phases?
    # Derivative constants
    num_paths = n_distinct_paths * len(condition_names)
    n_rounds_per_path = n_phases * n_periods_per_phase + 1
    num_rounds = (
        n_distinct_paths * n_periods_per_phase * n_phases * len(condition_names)
        + n_distinct_paths * len(condition_names) * 2
    )
    # The parameters for the price path
    up_probs = [0.35, 0.65]  # The possible probabilities of a price increase (i.e. "drifts")
    start_price = 1000  # The first price in the price path
    updates = [5, 10, 15]  # List of possible price movements
    starting_cash = 50000  # How much cash does the participant own at the start
    # Time:
    update_time = 5  # Number of seconds to show the price updates
    max_time = 7  # Number of seconds until a reminder to decide appears
    max_time_beliefs = 5  # Same but for the belief page
    experimenter_email = 'k.trutmann@unibas.ch'
    # Bot testing:
    bot_base_alpha = 0.2  # What's the base learning rate for the RL model
    bot_learning_effect = 0.04  # How much should the learning rate change for the model bot?
    show_debug_msg = False  # Whether to print current states to the console

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    transaction = models.IntegerField(label='')
    time_to_order = models.FloatField()
    unfocused_time_to_order = models.FloatField()
    changed_mind = models.BooleanField()
    erroneous_trade = models.StringField()
    belief = models.IntegerField(min=0, max=100, label='')
    time_to_belief_report = models.FloatField()
    unfocused_time_to_belief_report = models.FloatField()
    update_time_used = models.FloatField()
    price = models.IntegerField()
    cash = models.IntegerField()
    hold = models.IntegerField()
    base_price = models.FloatField()
    returns = models.IntegerField()
    final_cash = models.CurrencyField()
    i_round_in_path = models.IntegerField()
    investable = models.BooleanField()
    global_path_id = models.IntegerField()
    distinct_path_id = models.IntegerField()
    drift = models.FloatField()
    condition_name = models.StringField()
    completion_code = models.StringField(default='0000')


# FUNCTIONS
def make_price_paths(player: Player, n_distinct_paths):
    """
    This method first creates distinct movement sets and then multiplies and scrambles them
    (paths within the experiment and movements within phases). In the end it applies the movement sets
    to create the actual price paths. It takes constants as arguments so it can also be used for the training
    rounds.
    """
    # Determine the drift for each path:
    if player.participant._is_bot:
        rd.seed(5341 + player.participant.id_in_session)
    drift_list = rd.choices(player.participant.vars['up_probs'], k=n_distinct_paths)
    distinct_path_moves_list = []  # Will be a list of lists
    for this_drift in drift_list:
        moves = []
        for _ in range(Constants.n_rounds_per_path):
            movement_direction = rd.choices([1, -1], weights=[this_drift, 1 - this_drift])[0]
            movement_magnitude = rd.choice(Constants.updates)
            moves += [movement_direction * movement_magnitude]
        distinct_path_moves_list += [moves]
    all_moves_list = [copy.deepcopy(distinct_path_moves_list) for _ in Constants.condition_names]
    all_drifts_list = [copy.deepcopy(drift_list) for _ in Constants.condition_names]
    # If wanted, scramble the moves differently for each condition:
    if Constants.scramble_moves_in_phases:
        # The levels here are [condition][path][period]
        for i_cond, _ in enumerate(Constants.condition_names):
            for i_path in range(n_distinct_paths):
                # Create a moving window to scramble the movements:
                for i_phase in range(Constants.n_phases):
                    win_start_ix = i_phase * player.participant.vars['n_periods_per_phase']
                    win_end_ix = (i_phase + 1) * player.participant.vars['n_periods_per_phase']
                    these_moves = all_moves_list[i_cond][i_path][win_start_ix:win_end_ix]
                    rd.shuffle(these_moves)
                    all_moves_list[i_cond][i_path][win_start_ix:win_end_ix] = these_moves
    # Now also shuffle the paths together with their drifts:
    distinct_path_ids = [list(range(n_distinct_paths))] * len(Constants.condition_names)
    for i_cond, _ in enumerate(Constants.condition_names):
        these_ids = distinct_path_ids[i_cond].copy()
        rd.shuffle(these_ids)
        distinct_path_ids[i_cond] = these_ids
        all_drifts_list[i_cond] = [
            all_drifts_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]
        ]
        all_moves_list[i_cond] = [
            all_moves_list[i_cond][path_id] for path_id in distinct_path_ids[i_cond]
        ]
    # Apply the price movements to create actual prices and save them in the participant vars:
    # Not too elegant with the for loops, but it does the trick... ¯\_(ツ)_/¯
    prices = []
    i_path_global = 0
    i_path_global_list = []
    i_round_in_path = []
    distinct_path_id = []
    drift = []
    i_condition = []
    last_trial_in_path = []
    for i_cond, _ in enumerate(Constants.condition_names):
        for i_path in range(n_distinct_paths):
            prices += [Constants.start_price]
            i_path_global_list += [i_path_global]
            distinct_path_id += [distinct_path_ids[i_cond][i_path]]
            i_round_in_path += [0]
            drift += [all_drifts_list[i_cond][i_path]]
            i_condition += [i_cond]
            last_trial_in_path += [False]
            for i_move, this_move in enumerate(all_moves_list[i_cond][i_path]):
                prices += [prices[-1] + this_move]
                i_path_global_list += [i_path_global]
                distinct_path_id += [distinct_path_ids[i_cond][i_path]]
                i_round_in_path += [i_move + 1]
                drift += [all_drifts_list[i_cond][i_path]]
                i_condition += [i_cond]
                last_trial_in_path += [False]
            i_path_global += 1
            last_trial_in_path[-1] = True
    condition_name = [Constants.condition_names[i] for i in i_condition]
    price_df = pd.DataFrame(
        dict(
            global_path_id=i_path_global_list,
            distinct_path_id=distinct_path_id,
            i_round_in_path=i_round_in_path,
            last_trial_in_path=last_trial_in_path,
            price=prices,
            drift=drift,
            condition_id=i_condition,
            condition_name=condition_name,
        )
    )
    if Constants.shuffle_conditions:
        grouped_df = [group.copy() for _, group in price_df.groupby('global_path_id')]
        rd.shuffle(grouped_df)
        price_df = pd.concat(grouped_df.copy()).reset_index(drop=True)
    # Note: Django breaks when generating new price paths and storing them as pandas df since it's trying to compare
    # two dfs with different indexes. So I only use pandas for the condition scrambling and go back to dicts.
    player.participant.vars['price_info'] = price_df.to_dict(orient='list')
    if Constants.show_debug_msg:
        print('### Created Price Paths!')
        pd.set_option('display.max_rows', None)
        print(price_df)


def initialize_round(player: Player, n_distinct_paths):
    # If this is the very first round
    if player.round_number == 1:
        # This is needed so bot-testing can manipulate these values:
        if not player.participant._is_bot:
            player.participant.vars['up_probs'] = Constants.up_probs.copy()
            player.participant.vars['n_periods_per_phase'] = Constants.n_periods_per_phase

        make_price_paths(player, n_distinct_paths=n_distinct_paths)
        player.participant.vars['earnings_list'] = []
        player.global_path_id = 1
        # Decide what the initial hold will be for each path:
        if player.participant._is_bot:
            rd.seed(5341 + player.participant.id_in_session)
        initial_holds_per_path = [rd.choice(
            list(range(Constants.hold_range[0], 0))
            + list(range(1, Constants.hold_range[1] + 1))) for  # This makes sure 0 isn't chosen!
            _ in range(n_distinct_paths)]
        all_initial_holds = [initial_holds_per_path[i] for i in
            player.participant.vars['price_info']['distinct_path_id']]
        player.participant.vars['initial_holds'] = all_initial_holds

    else:
        player.global_path_id = player.in_round(player.round_number - 1).global_path_id
    # Record the relevant price variables into the database:
    for this_var in ['price', 'drift', 'condition_name', 'i_round_in_path', 'distinct_path_id']:
        setattr(
            player,
            this_var,
            player.participant.vars['price_info'][this_var][player.round_number - 1],
        )
    player.investable = is_investable(player)
    # If this is the first round of a new path:
    if player.i_round_in_path == 0:
        player.hold = player.participant.vars['initial_holds'][player.round_number - 1]
        player.cash = Constants.starting_cash - (player.hold * Constants.start_price)
        player.base_price = Constants.start_price if player.hold != 0 else 0
        player.returns = 0
        player.price = Constants.start_price
        if player.round_number > 1:
            player.global_path_id = player.in_round(player.round_number - 1).global_path_id + 1
    else:
        former_self = player.in_round(player.round_number - 1)
        if former_self.field_maybe_none('transaction') is None:
            former_self.transaction = 0
        player.hold = former_self.hold + former_self.transaction
        player.cash = (
            former_self.cash
            - former_self.transaction
            * player.participant.vars['price_info']['price'][player.round_number - 2]
        )
        # Base price:
        if player.hold == 0:
            player.base_price = 0
        elif (player.hold > 0) is not (former_self.hold > 0):  # "Crossed" the 0 hold line
            player.base_price = player.participant.vars['price_info']['price'][
                player.round_number - 2
            ]
        elif (
            former_self.transaction == 0 or abs(former_self.hold) - abs(player.hold) > 0
        ):  # Only sales or nothing
            player.base_price = former_self.base_price
        else:
            player.base_price = (
                abs(former_self.hold) * former_self.base_price
                + abs(former_self.transaction)
                * player.participant.vars['price_info']['price'][player.round_number - 2]
            ) / abs(player.hold)
        player.returns = int(
            player.hold
            * (
                player.participant.vars['price_info']['price'][player.round_number - 1]
                - player.base_price
            )
        )
        # If this is the last round of a block:
        if player.participant.vars['price_info']['last_trial_in_path'][player.round_number - 1]:
            # "Sell everything" for the last price:
            player.final_cash = (
                player.cash
                + player.hold
                * player.participant.vars['price_info']['price'][player.round_number - 1]
            )
            player.payoff = player.final_cash - Constants.starting_cash
            player.participant.vars['earnings_list'].append(player.payoff)
    if Constants.show_debug_msg:
        print('### Initialized round {} ################'.format(player.round_number))


# For displaying the page
def is_investable(player: Player):
    """Find out whether the participant should be able to make an investment decision in this round."""
    is_phase_start = (
        player.i_round_in_path % player.participant.vars['n_periods_per_phase'] == 0
        and not player.i_round_in_path == 0
    )
    is_first_phase = player.i_round_in_path < player.participant.vars['n_periods_per_phase']
    is_last_round = player.i_round_in_path == Constants.n_rounds_per_path 
    is_blocked_condition = player.condition_name in ['blocked_full_info', 'blocked_blocked_info']
    is_investable = ((not (is_first_phase or is_blocked_condition)) or is_phase_start) and not is_last_round
    if Constants.show_debug_msg:
        print('### Checked investablility: {}'.format(is_investable))
    return is_investable


def should_display_infos(player: Player):
    """Figures out whether this is a 'blocked info' trial, and should therefore be completely skipped."""
    last_round = player.participant.vars['price_info']['last_trial_in_path'][
        player.round_number - 1
    ]
    start_of_phase = player.i_round_in_path % player.participant.vars['n_periods_per_phase'] == 0
    blocked_condition = player.condition_name == 'blocked_blocked_info'
    first_phase = player.i_round_in_path < player.participant.vars['n_periods_per_phase']
    should_display = ((not blocked_condition) or first_phase or start_of_phase) and not last_round
    if Constants.show_debug_msg:
        print('### should_display_infos(): {}'.format(should_display))
    return should_display


def get_investment_span(player: Player):
    """Given you can invest in this round, how many periods into the future is this investment for?"""
    if player.condition_name == 'full_control':
        return 1
    elif player.condition_name in ['blocked_full_info', 'blocked_blocked_info']:
        return (
            player.participant.vars['n_periods_per_phase']
            if (player.i_round_in_path + 1) < Constants.n_rounds_per_path
            else 1
        )


def get_trading_vars(player: Player):
    percentage_returns = 0
    if player.base_price != 0:
        percentage_returns = round((player.returns / player.base_price) * 100, 1)
    if player.returns > 0:
        return_color = 'limegreen'
    elif player.returns < 0:
        return_color = 'red'
    else:
        return_color = 'black'
    return {
        'disp_base_price': round(player.base_price, 2),
        'return_color': return_color,
        'percentage_returns': percentage_returns,
        'all_val': player.price * player.hold,
        'wealth': int(player.price * player.hold + player.cash),
        'condition': player.participant.vars['price_info']['condition_name'][
            player.round_number - 1
        ],
        'investable': is_investable(player),
        'n_periods_to_invest': get_investment_span(player),
    }


def make_update_list(player: Player):
    """Creates a zipped list for django to display as the updates. The length depends on the condition."""
    if (
        player.condition_name == 'blocked_blocked_info'
        and player.i_round_in_path == player.participant.vars['n_periods_per_phase']
    ):
        # We are at the last decision of the blocked and low info condition, so show a list of updates:
        price_list = player.participant.vars['price_info']['price']
        # This is shown right after the blocked trade has been made. Hence "future".
        future_indexes = range(
            player.round_number - 1, player.round_number + player.participant.vars['n_periods_per_phase'] - 1
        )
        was_increase = [price_list[i + 1] > price_list[i] for i in future_indexes]
        differences = [abs(price_list[i + 1] - price_list[i]) for i in future_indexes]
        new_price = [price_list[i + 1] for i in future_indexes]
        return zip(was_increase, differences, new_price)
    else:
        was_increase = (
            player.participant.vars['price_info']['price'][player.round_number] > player.price
        )
        difference = abs(
            player.participant.vars['price_info']['price'][player.round_number] - player.price
        )
        new_price = player.participant.vars['price_info']['price'][player.round_number]
        return zip([was_increase], [difference], [new_price])


# In the very last round, calculate how much was earned
def calculate_final_payoff(player: Player):
    if Constants.show_debug_msg:
        print('##### Earnings list is {}'.format(player.participant.vars['earnings_list']))
    # Add the base_payoff to the game-payoff and make sure that it is floored at 0
    player.participant.payoff = cu(
        player.session.config['base_bonus'] / player.session.config['real_world_currency_per_point']
        + sum(player.participant.vars['earnings_list'])
    )
    if player.participant.payoff < 0:
        player.participant.payoff -= player.participant.payoff  # For some reason 0 didn't work.

    player.completion_code = ''.join(rd.sample(string.ascii_uppercase + '1234567890', k = 5))

    player.participant.vars['payoff_dict'] = {
        'payoff_list': zip(player.participant.vars['earnings_list']),
        'end_cash_sum': sum(player.participant.vars['earnings_list']),
        'payoff_total': player.participant.payoff_plus_participation_fee(),
        'showup_fee': player.session.config['participation_fee'],
        'base_payoff': player.session.config['base_bonus'],
        'percent_conversion': round(
            player.session.config['real_world_currency_per_point'] * 100, 2),
        'completion_code': player.completion_code
    }


# PAGES
class initializer_page(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        initialize_round(player, n_distinct_paths=Constants.n_distinct_paths)


class condition_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.i_round_in_path == 0

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'drift_list': [round(i * 100) for i in Constants.up_probs],
            'periods_per_phase': Constants.n_periods_per_phase,
            'exp_email': Constants.experimenter_email,
        }


class trading_page(Page):
    form_model = 'player'
    form_fields = [
        'transaction',
        'time_to_order',
        'unfocused_time_to_order',
        'changed_mind',
        'erroneous_trade',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return should_display_infos(player)

    @staticmethod
    def vars_for_template(player: Player):
        return get_trading_vars(player)


class belief_page(Page):
    form_model = 'player'
    form_fields = ['belief', 'time_to_belief_report', 'unfocused_time_to_belief_report']

    @staticmethod
    def is_displayed(player: Player):
        return should_display_infos(player)

    @staticmethod
    def vars_for_template(player: Player):
        return {'max_time': Constants.max_time_beliefs}


class update_page(Page):
    form_model = 'player'
    form_fields = ['update_time_used']

    @staticmethod
    def is_displayed(player: Player):
        return should_display_infos(player)

    @staticmethod
    def get_timeout_seconds(player: Player):
        # Give more time if a list is presented:
        return (
            Constants.update_time * 2
            if player.condition_name == 'blocked_blocked_info'
            and player.i_round_in_path == Constants.n_periods_per_phase
            else Constants.update_time
        )

    @staticmethod
    def vars_for_template(player: Player):
        return {'update_list': make_update_list(player)}


class end_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_final_payoff(player)


page_sequence = [
    initializer_page,
    condition_page,
    trading_page,
    belief_page,
    update_page,
    end_page,
]
