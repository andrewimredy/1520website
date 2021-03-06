#!/usr/bin/python3
from flask import Flask, render_template, session, request, redirect, jsonify
from google.cloud import datastore
from auth import blue as auth_blueprint, get_user
from user import userStore, generate_creds, hash_password
from groups import GroupInfo, create_group, join_group, get_data_of_members, get_groups_user_is_in, get_all_users
import time, atexit
from apscheduler.schedulers.background import BackgroundScheduler

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
    ### newlist contains all teams playing. ([0][0][gameId] vs [0][1], [1][0] vs [1][1])


def get_bets_for_user(user):
    #get unfinished bets for the user
    query = datastore_client.query(kind='bet')
    query.add_filter("user" , "=" , user)
    bets = list(query.add_filter('result', '=', 'none').fetch())
    return bets

##atomatic updating:
scheduler = BackgroundScheduler()
scheduler.add_job(func=backend.update_games, trigger='interval', seconds=600)
scheduler.add_job(func=backend.update_bets, trigger='interval', seconds=600)
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def main_page():
    scheduler.start()
    user = get_user()
    get_game_info()
    return render_template("index.html", newlist=newlist, numgames=numgames,  timelist=timelist, user=user)

@app.route('/bet/<game>/<team>', methods=['POST']) #places bet, called by js on click
def place_bet(game, team):
    if not get_user():
        return redirect('/auth/login')
    entity_key = datastore_client.key('bet', get_user() + game)
    bet_entity = datastore.Entity(key=entity_key)
    if(team == 'v'):
        teamFull = 'visitor'
    elif(team == 'h'):
        teamFull = 'home'
    bet_entity['team'] = teamFull #home or visitor
    bet_entity['user'] = get_user()
    bet_entity['game'] = game
    bet_entity['result'] = 'none'
    datastore_client.put(bet_entity)
    return jsonify(success=True)
   


@app.route('/Profile')
def profile_view():
    return render_template("profile.html")

@app.route('/myStats')
def stats_view():
    user = get_user()
    groups = list()
    games = list()
    if user:
        points = get_points(user)
        groupNames = get_groups_user_is_in(user)
        bets = get_bets_for_user(user)        
        for group in groupNames:
            groups.append(get_data_of_members(group))
        for bet in bets:
            game_curr = datastore_client.get(datastore_client.key('game', bet['game']))
            games.append(game_curr)
        return render_template("myStats.html" , user=user , points=points , groups=groups , groupNames=groupNames , bets=bets , games=games)
    return render_template("myStats.html" , user=user)

def get_points(userStr):
    user_key = userstore.ds.key("userCreds", userStr)
    user = userstore.ds.get(user_key)
    return user["points"]

@app.route('/groups')
def groups_view():
    user = get_user()
    groups = list()
    if not user:
        return redirect("/auth/login")
    groupNames = get_groups_user_is_in(user) #returns a list
    for group in groupNames:
        groups.append(get_data_of_members(group))
    groupNames.insert(0, "Global LeaderBoard")
    groups.insert(0, get_all_users())   
    listForJavascript = convertToList(groups)
    return render_template("groups.html", groups=groups, user=user, groupNames = groupNames, listForJavascript = listForJavascript, numberOfGroups = len(groupNames))

def convertToList(groups):
    newGroups = []
    for group in groups:
        newGroup = []
        newGroups.append(newGroup)        
        for member in group:
            newMember = []
            newMember.append(member['username'])
            newMember.append(member['points'])
            newGroup.append(newMember)
    return newGroups

@app.route('/groups/create_group', methods=["GET"])
def create_group_view():
    return render_template("create_group.html")

@app.route('/groups/create_group', methods=["POST"])
def create_group_post():
    group_name = request.form.get("group_name")
    max_size = request.form.get("max_size")
    username = get_user()
    password = request.form.get("password")
    create_group(group_name, max_size, password, username)
    return redirect("/groups")

@app.route('/groups/join_group', methods=["GET"])
def join_group_view():
    return render_template("join_group.html")

@app.route('/groups/join_group', methods=["POST"])
def join_group_post():
    group_name = request.form.get("group_name")
    username = get_user()    
    password = request.form.get("group_password")    
    join_group(group_name, username, password)
    return redirect("/groups")
