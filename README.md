# LattRank

This script queries each leaderboard from Hades, filtered to most relevant subcategories, and ranks each runner by LattRank.

1st place in a category = 10 points
10th place in a category = 1 point

It uses a sqlite database to reduce number of API calls, but the first run will take a long time to collect user names.

It also tracks when it was last run, and checks whether there are any new runs verified, otherwise it just dumps out the most recent scores.

## To run the script

Just run `python3 main.py`

## In the future

We can just automatically build variable maps by parsing the results of `/api/v1/games/{id}/variables` but that was a little too annoying to deal with for a first pass. If we set that up, though, we can expand this to any game with very little further effort.
