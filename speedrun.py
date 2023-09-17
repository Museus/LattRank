from collections import defaultdict
import requests
import itertools
import time

from database import db
from hades import CATEGORIES, SUBCATEGORIES, GAME_ID, TIMINGS, IGNORE
from hades_map import SUBCATEGORIES_MAP, TIMINGS_MAP

VERBOSE = False

def log(msg):
    if VERBOSE:
        log(msg)

user_leaderboard = defaultdict(lambda: {"score": 0, "runs": {}})
user_points = defaultdict(int)

db.initialize()

print("Getting all run data...")

for category_name, category_id in CATEGORIES.items():
    log(category_name)
    keys, values = zip(*SUBCATEGORIES[category_name].items())
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
    for combination in permutations_dicts:
        for timing in TIMINGS[category_name]:

            skip_this_one = False

            mapped_subcategories = [SUBCATEGORIES_MAP[category_name][(var_id, var_value)] for var_id, var_value in combination.items()]
            all_filters = mapped_subcategories + [TIMINGS_MAP[timing]]

            subcategory_pub_string = ", ".join(mapped_subcategories)
            for illegal_category in IGNORE.get(category_name, []):
                if all(illegal_value in all_filters for illegal_value in illegal_category):
                    log(f"  -- Skipping {TIMINGS_MAP[timing]}, {subcategory_pub_string}")
                    skip_this_one = True

            if skip_this_one:
                continue

            subcategory_var_string = "&".join([f"var-{var_id}={var_value}" for var_id, var_value in combination.items()])
            subcategory_pub_string = ", ".join([SUBCATEGORIES_MAP[category_name][(var_id, var_value)] for var_id, var_value in combination.items()])

            log(f"  + Getting {TIMINGS_MAP[timing]}, {subcategory_pub_string}  [ /api/v1/leaderboards/{GAME_ID}/category/{category_id}?top=100&{subcategory_var_string}&timing={timing} ]")
            connection_string = f"https://speedrun.com/api/v1/leaderboards/{GAME_ID}/category/{category_id}?top=100&{subcategory_var_string}&timing={timing}"

            top_x_runs = requests.get(connection_string).json()
            unique_players = set()

            for run in top_x_runs["data"]["runs"]:
                user_id = run["run"]["players"][0]["id"]
                if user_id in unique_players:
                    continue

                user_leaderboard[user_id]["score"] += 10 - len(unique_players)
                user_leaderboard[user_id]["runs"][run["run"]["weblink"]] = (f"{category_name} ({TIMINGS_MAP[timing]}, {subcategory_pub_string})", 10 - len(unique_players))
                unique_players.add(user_id)
                if len(unique_players) == 10:
                    break

place_width = len(str(len([user for user in user_leaderboard.keys() if user_leaderboard[user]["score"] >= 5]))) + 1

for place, user_id in enumerate(sorted(user_leaderboard, key=lambda x: user_leaderboard[x]["score"], reverse=True)):
    user_name = db.get_user_name_by_id(user_id)
    if not user_name:
        user_name = requests.get(f"https://speedrun.com/api/v1/users/{user_id}").json()["data"]["names"]["international"]
        db.add_user(user_id, user_name)
        time.sleep(1)

    if user_leaderboard[user_id]['score'] < 5:
        break

    print(f"{str(place+1).rjust(place_width)} - {user_name} - {user_leaderboard[user_id]['score']}")
