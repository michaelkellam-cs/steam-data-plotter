import requests as rq
import json

# Not necessary, but just put just in case. This is for the Steam key. Put your steam key in if you'd like.
key = "1"

apps = None

# Retrieves player count of game given the appid
def player_count(app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=" + str(app_id) + "&?key=" + key + "&?format=json"
    data = rq.get(url).json()
    return data['response']['player_count'] 

# Returns the name of the game given the appid
def game_name(app_id):
    global apps
    if apps is None:
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v02/?key=" + key + "&format=json"
        data = rq.get(url).json()
        apps = data['applist']['apps']
        print('dont have')
    else:
        print('have')
    for i in apps:
        if i['appid'] == app_id:
            return i['name']
        
# Debugging command, simply states the game name and the number of players
def name_pair(app_id):
    pc = player_count(app_id)
    name = game_name(app_id)
    
    print("The game " + name + " has " + str(pc) + " current players")
    return
    
        