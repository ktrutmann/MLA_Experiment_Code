# Trading_Task
This is a trading task similar to Weber & Camerer (1998).

## Settings

### Experimental Flow
- `n_periods_per_phase`: How long should the participants be "blocked"?
- `n_distinct_paths`: How many paths should be generated for each condition?
The actual amount of paths played by the participants is thus multiplied
by the number of conditions.
- `condition_names`: A list of all the conditions that should be played
- `n_phases`: A list indicating for each condition in `condition_names` how many
phases it contains.
- `hold_range`: A list containing the minimum and maximum amount of shares that can be held.
- `shuffle_conditions`: Should the conditions be presented in "blocks" or shuffled?
If they are shuffled, the condition page will be displayed each time the condition changes.

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

### Other:
- `experimenter_email`: Can be displayed in case something goes wrong so
participants can contact you.
- `bot_type`: Given browser bots are active, this string will determine how they behave.
`'optimal'` will lead to rational behavior. `'model'` leads to a reinforcement learning
model being used to generate the answers. `'random'` will provide random answers.
Lastly, `'custom'` returns extreme answers that
simulate the desired effect of the study for sanity checking the analysis script with the
generated data.

## Experiment Code
Because of the way oTree handles the round numbers (beginning with 1), the indices of 
periods and prices are shifted by one. So in round 1 price number 0 is displayed,
and the price update that will be displayed is from 0 to 1. In the last round (n) the price
is updated from price number n-1 to n. Further, to have all conditions within one app, there is a
parallel "round management system". The variables for this are stored in the `participant.vars` dict:

- `i_in_block` is the round number within this block (path) starting from 0.
- `i_block` the global index of the current path starting from 0.
- `condition` tracks the current condition name.
- `skipper` is set to true to skip the last round of each block. This is because the price path
will move one last time in the end but that should not be a "tradeable" round.

The information about the price and their conditions is saved in a pandas dataframe in
`participant.vars['price_info']`. It contains the following columns:

- `global_path_id`: Unique ID for each new path.
- `distinct_path_id`: ID that identifies which path this scrambled path stemmed from
- `price`: Current price in this path
- `drift`: What the up-drift for this path was
- `condition_id`: ID of the condition this path is supposed to be used for
- `condition_name`: Name of the condition this path is supposed to be used for


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
        changed_mind = models.BooleanField(default=False) 
    erroneous_trades = models.IntegerField() 

    bayes_prob_up = models.FloatField()
    state = models.BooleanField()
    belief = models.IntegerField(min=0, max=100, widget=widgets.Slider, label='')
    belief_bonus = models.CurrencyField()
    belief_bonus_cumulative = models.CurrencyField()
    price = models.IntegerField()
    drift = models.FloatField()

    condition = models.StringField()
    i_round_in_block = models.IntegerField()
    global_path_id = models.IntegerField()
    distinct_path_id = models.IntegerField()
    investable
