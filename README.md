# Football Cards Prediction ⚽

A beginner-friendly Machine Learning project that estimates next-season yellow and red card counts from historical player-season statistics.

## Project goals
- Aggregate match-level appearances into player-season statistics.
- Predict next-season yellow and red card counts.
- Compare Linear Regression and Random Forest.
- Use a chronological holdout season rather than a random split.
- Compare model performance with a simple zero-card baseline.
- Look up a player and generate estimates from their latest available season record.

## Dataset
Expected filename: `appearances-selected-columns.csv`

The notebook uses these columns:
- `game_id`
- `player_id`
- `date`
- `player_name`
- `yellow_cards`
- `red_cards`

The provided dataset covers **2012-07-03 through 2021-02-06**. The 2020 season is incomplete, so it is excluded as a target season. The notebook does not include the CSV in this repository package; add it separately when running the notebook.

**Before publishing publicly:** add the original dataset source URL and confirm that its license allows redistribution or public use. Do not claim a source or license unless you have verified it.

## Method
1. Parse dates and define seasons as starting in August.
2. Aggregate match-level rows into player-season totals.
3. Build next-season targets only where the player's source and target seasons are consecutive.
4. Train on source seasons through 2017 and hold out source season 2018 (target season 2019) for evaluation.
5. Compare Linear Regression, Random Forest, and a zero-card baseline using MAE, RMSE, and R².
6. Fit final regression models on labeled examples with target seasons through 2019 for the lookup demo.

## Holdout results

Metrics from the supplied dataset, on the held-out target season 2019:

| Target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Yellow cards | Linear Regression | 2.0656 | 2.6419 | 0.2436 |
| Yellow cards | Random Forest | 2.0867 | 2.6845 | 0.2190 |
| Yellow cards | Zero baseline | 3.2804 | 4.4709 | -1.1662 |
| Red cards | Linear Regression | 0.1457 | 0.2824 | 0.0036 |
| Red cards | Random Forest | 0.1474 | 0.2887 | -0.0413 |
| Red cards | Zero baseline | 0.0781 | 0.2935 | -0.0761 |

**Interpretation:** Linear Regression performs best among the tested models for yellow cards, but its average absolute error is still about 2.07 cards. For red cards, the zero-card baseline has a lower MAE than either regression model. This means the red-card model has not demonstrated useful improvement over the simple baseline; do not claim that it predicts red cards accurately.

These results are educational and specific to this dataset and split. They are not a guarantee of future performance.

## Run in Google Colab
1. Upload `football_cards_prediction.ipynb` to Google Colab.
2. Run the cells from top to bottom.
3. When prompted by the notebook, upload `appearances-selected-columns.csv`.
4. In the final cell, change `PLAYER_NAME` to a player name you want to test.

## Requirements
See `requirements.txt`.

## Limitations
- The dataset is historical and ends on 2021-02-06.
- The 2020 season is incomplete in the supplied data.
- Only three features are used: appearances, yellow cards, and red cards in the source season.
- Player performance can change due to position, minutes played, competition, team, and other factors not included here.
- Red cards are rare in the data and the current models do not beat the zero-card baseline on MAE.
- Predictions are estimates, not guaranteed outcomes.

## Future improvements
- Add richer features such as minutes played, position, age, competition, and team.
- Compare against stronger and better-calibrated count models.
- Use multiple chronological evaluation windows.
- Investigate player transfers and missing seasons.
