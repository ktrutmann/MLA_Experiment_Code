# Trading_Task
This is a trading task similar to Weber & Camerer (1998).

## Settings

### Experimental Flow
- `n_phases`: How many phases should there be?
- `n_periods_per_phase`: How long should the participants be "blocked"?
- `n_distinct_paths`: How many paths should be generated for each condition?
The actual amount of paths played by the participants is thus multiplied
by the number of conditions.
- `condition_names`: A list of all the conditions that should be played
- `hold_range`: A list containing the minimum and maximum amount of shares that can be held.

### Price Path Parameters
- `up_probs`: List of the possible probabilities of a price increase (i.e. "drifts")
- `start_price`: The first price in the price path
- `updates`: List of possible price movements
- `starting_cash`: How much cash does the participant own at the start

### Belief Elicitation
- `max_belief_bonus`: How much can be won and bet in the belief elicitation?
- `belief_bonus_discount`: How many "investment points are the belief points worth?

### Time Limits
- `update_time`: Indicated how long the updating screen is shown.
- `max_time`: Indicates how long the trading screen is shown before a warning appears
- `max_time_beliefs`: Indicates how long the belief elicitation screen is shown before a warning appears


## Experiment Code
Because of the way oTree handles the round numbers (beginning with 1), the indices of 
periods and prices are shifted by one. So in round 1 price number 0 is displayed,
and the price update that will be displayed is from 0 to 1. In the last round (n) the price
is updated from price number n-1 to n. Further, to have all conditions within one app, there is a
parallel "round management system". The variables for this are stored in the `participant.vars` dict:

- `i_in_block` is the round number within this block (condition) starting from 0.
- `i_block` the index of the condition in the condition_sequence starting with 0.
- `condition` tracks the current condition name.
- `skipper` is set to true to skip the last round of each block. This is because the price path
will move one last time in the end but that should not be a "tradable" round.


## Exported Data (Codebook)
All variables represent the state of the world at the start of one period.
The exception are the decision variables such as `transaction`, `erronious_trade` and the
`changed_mind` variable which represent actions taken during the trading period.

- `time_to_order`: How many seconds it took from loading the page to submitting the order?
- `unfocused_time_to_order`: How many seconds was the participant away from the trading page while it was loaded.
Optimally this is always 0.


- `cash`: Cash holdings at the start of the period
- `final_cash`: The final cash earnings after the last period and after all
assets have been sold. Should be empty except for the last period.
- `hold`: Whether the asset was held at the start of the current period.
- `return`: The current *paper* returns of the asset. As soon as the asset
is sold, the return is reset to 0.
- `transaction`: -1 being a sell, 1 being a buy and 0 being doing nothing.
- `base_price`: The price for which the asset was bought, if held.

 __TODO:__ Add all these variables:
 
    time_to_belief_report = models.FloatField()
    unfocused_time_to_belief_report = models.FloatField()
    update_time_used = models.FloatField()

    bayes_prob_up = models.FloatField()
    state = models.BooleanField()
    belief = models.IntegerField(min=0, max=100, widget=widgets.Slider, label='')
    belief_bonus = models.CurrencyField()
    belief_bonus_cumulative = models.CurrencyField()
    price = models.IntegerField()

    condition = models.StringField()
    i_round_in_block = models.IntegerField()
    i_block = models.IntegerField()