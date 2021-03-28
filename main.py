#!/usr/bin/python3
from flask import Flask, render_template
app = Flask(__name__)


### API INTERACTION ###
import requests, json, backend

timelist = [] #list of game times
newlist = [] # list of games eg: ["Philadelphia 76ers", "Boston Celtics"]
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
        teamlist.append([json2['games'][game]['vTeam']['triCode'], json2['games'][game]['hTeam']['triCode']])
    for game in range(numgames):
        timelist.append(json2['games'][game]['startTimeEastern'])
    for i in teamlist:
        newlist.append([get_full_name(i[0]), get_full_name(i[1])])
    ### newlist contains all teams playing. ([0][0] vs [0][1], [1][0] vs [1][1])



@app.route('/')
def main_page():
    get_game_info()
    return render_template("index.html", newlist=newlist, numgames=numgames,  timelist=timelist)

@app.route('/Profile')
def profile_view():
    return render_template("profile.html")

@app.route('/myStats')
def stats_view():
    return render_template("myStats.html")

@app.route('/groups')
def groups_view():
    return render_template("groups.html")
