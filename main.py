#!/usr/bin/python3
from flask import Flask, render_template, session
from google.cloud import datastore
from auth import blue as auth_blueprint
from user import userStore, generate_creds, hash_password

app = Flask(__name__)
app.secret_key = b"7131791ae45df500d74730c2c04f16439140977bff6cf792157a6c4e55b7"
app.register_blueprint(auth_blueprint, url_prefix="/auth")

datastore_client = datastore.Client()
userstore = userStore(datastore_client)

### API INTERACTION ###
import requests, json, backend

timelist = [] #list of game times
newlist = [] # list of games eg: ["Philadelphia 76ers", "Boston Celtics", "20034512"] visitor, home, id
numgames = 0

#Convenience method to turn abbreviation into full team name. declare this before using it
teams = (requests.get('http://data.nba.net/10s/prod/v2/2020/teams.json')).json()
def get_full_name(tricode):
    for team in range(30):
        if(teams['league']['standard'][team]['tricode'] == tricode):
            return teams['league']['standard'][team]['fullName']

def get_game_info():
    teamlist = []
    del newlist[:] #prevent duplicates
    del timelist[:]
    #get url of today's scoreboard.. easier this way than doing date stuff
    json1 = (requests.get('http://data.nba.net/10s/prod/v1/today.json')).json()
    url = (json1['links'])['currentScoreboard']
    url = 'http://data.nba.net/10s' + url
    #get json for today's scores
    json2 = (requests.get(url)).json()
    numgames = json2['numGames'] #number of games being playd today
    
    for game in range(numgames):
        teamlist.append([json2['games'][game]['vTeam']['triCode'], 
                         json2['games'][game]['hTeam']['triCode'],
                         json2['games'][game]['gameId']])
        timelist.append(json2['games'][game]['startTimeEastern'])
    for i in teamlist:
        newlist.append([get_full_name(i[0]), get_full_name(i[1]), i[2]])
    ### newlist contains all teams playing. ([0][0] vs [0][1], [1][0] vs [1][1])



@app.route('/')
def main_page():
    user = get_user()
    get_game_info()
    return render_template("index.html", newlist=newlist, numgames=numgames,  timelist=timelist, user=user)

@app.route('/bet/<game>/<team>')
def place_bet(game, team):
    entity_key = datastore_client.key('bet', username + game)
    bet_entity = datastore.Entity(key=entity_key)
    bet_entity['team'] = team #home or away
   

@app.route('/Profile')
def profile_view():
    return render_template("profile.html")

@app.route('/myStats')
def stats_view():
    user = get_user()
    if user:
        points = get_points(user)    
        return render_template("myStats.html" , user=user , points=points)
    return render_template("myStats.html" , user=user)

@app.route('/groups')
def groups_view():
    user = get_user()
    return render_template("groups.html", user=user)

def get_user():
    return session.get("user", None)

def get_points(userStr):
    user_key = userstore.ds.key("userCreds", userStr)
    user = userstore.ds.get(user_key)
    return user["points"]