import sys
import time
import datetime
import numpy as np
import pandas as pd
import steamapi as stm
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler

# main.py is responsible for gathering game data intermittenly,
# and saving the new data to an existing CSV, or creating a new CSV.

# This list refreshed each interval, and it will contain the list of
# appids inside games.txt
my_list = []

# Populates my_list from scratch, adding all existing appids in games.txt
def setup():
	global my_list
	my_list.clear()
	textfile = open('games.txt', 'r')
 
	# This loop takes each line and does some pruning (removes escape characters and spaces)
	for line in textfile:
		strip_ln = line.strip()
		print(strip_ln)
		my_list.append(strip_ln)
	
	run()

# This is the function that starts the process of adding new data to each appid that exists in games.txt
def run():
	global my_list
	for i in my_list:
		add_df(int(i))


# Adds new DataFrame data to either an existing CSV, or creates a new CSV file and adds the new data.
def add_df(appid):
	app_path = Path('./gamedata/' + str(appid) + '.csv')
	if app_path.is_file():
		df = pd.read_csv('./gamedata/' + str(appid) + '.csv',index_col=None)
	else:
		d = {'date_time': [], 'current players': [], 'rating': []}
		df = pd.DataFrame(data=d)
	frames = [df, stm.get_data(appid)]
	new_df = pd.concat(frames)
	new_df.to_csv(path_or_buf = './gamedata/' + str(appid) + '.csv',index=False)

# Creates the scheduler to allow for calling functions by interval.
scheduler = BlockingScheduler()
scheduler.add_job(setup,'interval',hours=1)
scheduler.start()