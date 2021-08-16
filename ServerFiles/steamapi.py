import requests as rq
import json
import pandas as pd
from datetime import datetime
from pytz import timezone

# This steamapi.py file is similar to the steamapi.py file for the client-side.
# I've decided to make them separate files so that I can edit each depending on what else
# I need to add for future updates/features.
# This is because most of these functions are needed to write the proper data.
# The client-side is not responsible for these types of tasks, only displaying the information.

# Optional Steam key. You may paste in your own here.
key = "1"

# Returns number of players given the appid
def player_count(app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=" + str(app_id) + "&?key=" + key + "&?format=json"
    data = rq.get(url).json()
    return data['response']['player_count']


# Gets a dictionary of all reviews: total, positive, and negative.
def total_reviews(app_id):
	url = 'http://store.steampowered.com/appreviews/' + str(app_id) + '?json=1'
	resp = rq.get(url)
	data = resp.text
	parsed = json.loads(data)

	preparse = parsed['query_summary']
	newdict = {
		'total_reviews': -1,
		'total_positive': -1,
		'total_negative': -1
	}

	newdict['total_reviews'] = preparse['total_reviews']
	newdict['total_positive'] = preparse['total_positive']
	newdict['total_negative'] = preparse['total_negative']

	return newdict


# Gets the rate of positive reviews, out of 1.0
# Example: if the a game has a review percentage of 87%, then the value returned from this would be 0.87
def review_rate(app_id):
	total_rev = total_reviews(app_id)
	return total_rev['total_positive'] / total_rev['total_reviews'] 


# Gets name of game given the appid
def game_name(app_id):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v02/?key=" + key + "&format=json"
    data = rq.get(url).json()
    apps = data['applist']['apps']
    for i in apps:
        if i['appid'] == app_id:
            return i['name']


def name_pair(app_id):
    pc = player_count(app_id)
    name = game_name(app_id)

    print("The game " + name + " has " + str(pc) + " current players")
    return


# Creates a DataFrame of:
# - Date/Time
# - Current Players
# - Game Rating
#
# This data is then put into a CSV file
# See: main.py, add_df() function
def get_data(app_id):
	pc = player_count(app_id)
	rating = review_rate(app_id)
	d = {'date_time': [datetime.now(timezone('America/New_York')).replace(tzinfo=None, microsecond=0)], 'current players': [pc], 'rating': [rating]}
	df = pd.DataFrame(data=d)
	print(df.to_string())
	return df
