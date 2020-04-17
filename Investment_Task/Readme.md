# Trading_Task
This is a trading task similar to Frydman, Barberis, Camerer, Bossaerts &
Rangel (2014). It uses a Markov-chain to generate an auto-correlated price paths
on which the participants can trade.

## Settings

- `main_condition`: Will the subject be shown the states or the probabilities?
Will be determined randomly if set to `random`.
This only determines the name of the informative column in the trading table.
- `condition_sequence`: In what order to display the different conditions. The possibilities are `'baseline'`,
`'probs_shown'`, where the bayesian probability of a price increase is shown and `'states_shown'` where the current
state is revealed.
subsequent pairs of two such that the updating can be measured.
- `n_periods_per_block`: How many trading periods should each condition have

- `update_time`: Indicated how long the updating screen is shown.
- `max_time`: Indicates how long the trading screen is shown before a warning appears
- `max_time_beliefs`: Indicates how long the belief elicitation screen is shown before a warning appears


The settings for generating the markov chain are commented in the code.
Further, the "starting portfolio" can also be set, meaning the amount of cash,
whether the asset is held or not at the start (it can also be set to be determined randomly)

## Price path
If the price path is provided, the path to a csv containing the paths must be given to `Constants.import_path`.
The file should only contain a `price` and a `good_state` column and should be a concatenation over all
Conditions, including the last round of each condition. Thus if there are three trading rounds of two conditions,
the file should have 8 rows (two times a starting price and three updates).

## Exported Data
The price paths that are generated for each participant are automatically
exported to the `price_paths` folder within the app folder.

All variables represent the state of the world at the start of one period.
The exception are the decision variables such as `transaction`, `erronious_trade` and the
`changed_mind` variable which represent actions taken during the trading period.

- `cash`: Cash holdings at the start of the period
- `final_cash`: The final cash earnings after the last period and after all
assets have been sold. Should be empty except for the last period.
- `hold`: Whether the asset was held at the start of the current period.
- `return`: The current *paper* returns of the asset. As soon as the asset
is sold, the return is reset to 0.
- `transaction`: -1 being a sell, 1 being a buy and 0 being doing nothing.
- `base_price`: The price for which the asset was bought, if held.
- `time_to_order`: How many seconds it took from loading the page to submitting the order?
- `unfocused_time_to_order`: How many seconds was the participant away from the trading page while it was loaded.
Optimally this is always 0.

## Code
Because of the way oTree handles the round numbers (beginning with 1), the indices of 
periods and prices are shifted by one. So in round 1 price number 0 is displayed,
and the price update that will be displayed is from 0 to 1. In the last round (n) the price
is updated from price number n-1 to n. Further, to have all conditions within one app, there is a
parallel "round management system". The variables for this are stored in the participant.vars dict:

is updated one last time, but no trades should be made in this round.
- `i_in_block` is the round number within this block (condition) starting from 0.
- `i_block` the index of the condition in the condition_sequence starting with 0.
- `condition` tracks the current condition name.
- `skipper` is set to true to skip the last round of each block. This is because the price path
