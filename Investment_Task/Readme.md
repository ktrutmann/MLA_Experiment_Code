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
- `extra_inv_phase`: Indicates for each entry of `condition_names` whether to ask for one last
investment after `n_periods_per_phase * n_phases` periods. 
- `hold_range`: A list containing the minimum and maximum amount of shares that can be held.
- `shuffle_conditions`: Should the conditions be presented in "blocks" or shuffled?
If they are shuffled, the condition page will be displayed each time the condition changes.
- `scramble_moves_in_phases`: Whether price moves should be scrambled within phases.
This would lead to prices arriving at the same points at the end of phase 1 and 2, but in
slightly different paths.

### Price Path Parameters
- `up_probs`: List of the possible probabilities of a price increase (i.e. "drifts")
- `start_price`: The first price in the price path
- `updates`: List of possible price movements
- `starting_cash`: How much cash does the participant own at the start

### Time Limits
- `update_time`: Indicated how long the updating screen is shown.
- `max_time`: Indicates how long the trading screen is shown before a warning appears
- `max_time_beliefs`: Indicates how long the belief elicitation screen is shown before a warning appears

### Other:
- `experimenter_email`: Can be displayed in case something goes wrong so
participants can contact you.

### Bot Testing:
- `bot_base_alpha`: When doing bot testing of the experiment and selecting the `'model'` case,
what should be the learning rate of the reinforcement learning model? 
- `bot_learning_effect`: How much less should the learning rate be in the interaction-situations
for the bot?


## Experiment Code
Because of the way oTree handles the round numbers (beginning with 1), the indices of 
periods and prices are shifted by one. So in round 1 price number 0 is displayed,
and the price update that will be displayed is from 0 to 1. In the last round (n) the price
is updated from price number n-1 to n.
There is also a "parallel" round count to manage the conditions and the round number _within_
the conditions. The variables that are used to manage this round and condition system are
described below as they are also exported to the data.


## Exported Data (Codebook)
All variables represent the state at the start of one period unless written otherwise.
The exception are the decision variables such as the `transaction` or `changed_mind` variables
which represent actions taken during the trading period.

***
- `transaction`: How much the participant decided to buy/sell in this round indicated as
an integer within `Constants.hold_range`.
- `time_to_order`: How many seconds it took from loading the page to submitting the order?
- `unfocused_time_to_order`: How many seconds was the participant away from the trading page while it was loaded.
Optimally this is always 0.
- `changed_mind`: Boolean variable indicating whether the "change order" button was used
or not.
- `erroneous_trade`: Records what "mistakes" the participant made (e.g. wanting to buy more
than what can maximally be held).

***
- `belief`: The reported belief about the probability of a price increase as a number
from 0 to 100.
- `time_to_belief_report` and `unfocused_time_to_belief_report`: See `time_to_order`.

***
- `update_time_used`: How long was the updating page displayed before the participant
clicked the "Next" button (if at all.)

***
- `price`: Current price in this path (at the _start_ of the period).
- `cash`: Cash holdings at the start of the period
- `hold`: Whether the asset was held at the start of the current period.
- `base_price`: The average price for which the asses were bought, if any are held.
- `returns`: The current *paper* returns of the asset. As soon as the asset
is sold, the return is reset to 0.
- `final_cash`: The final cash earnings after the last period and after all
assets have been sold. Should be empty except for the last period.

***
- `i_round_in_path` is the round number within this block (path) starting from 0.
- `investable`: Indicates whether the participant was given the option to trade in this
period or not.
- `global_path_id`: Unique ID for each new path.
- `distinct_path_id`: ID that identifies which path this scrambled path stemmed from.
Paths with the same `distinct_path_id` will have the same price at the periods between phases.
- `drift`: The probability of a price increase in this path.
- `condition_id`: ID of the condition this path is supposed to be used for.
- `condition_name`: Name of the condition this path is supposed to be used for.


# Bot Testing
Given browser bots are active, the `cases` attribute can be used to set which 
simulations should be run.
`'optimal'` will lead to rational behavior. `'model'` leads to a reinforcement learning
model being used to generate the answers (the learning parameters are set in the
`Constants`. `'random'` will provide random answers and belief reports.
Lastly, `'custom'` returns extreme answers that simulate the desired effect of
the study for sanity checking the analysis script with the generated data.