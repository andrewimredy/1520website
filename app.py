from flask import Flask, render_template, request, session, redirect
from groups import GroupInfo, create_group 
app = Flask(__name__)

### API INTERACTION ###
import requests, json
#get url of today's scoreboard.. easier this way than doing date stuff
json1 = (requests.get('http://data.nba.net/10s/prod/v1/today.json')).json()
url = (json1['links'])['currentScoreboard']
url = 'http://data.nba.net/10s' + url

#get json for today's scores .. hardcoded url for now b/c all star break
json2 = (requests.get(url)).json()
numgames = json2['numGames'] #number of games being playd today
teamlist = [] #list of teams playing today
for game in range(numgames):
    teamlist.append(json2['games'][game]['vTeam']['triCode'])
    teamlist.append(json2['games'][game]['hTeam']['triCode'])

timelist = [] #list of game times
for game in range(numgames):
    timelist.append(json2['games'][game]['startTimeEastern'])

#Convenience method to turn abbreviation into full team name. declare this before using it
teams = (requests.get('http://data.nba.net/10s/prod/v2/2020/teams.json')).json()
def get_full_name(tricode):
    for team in range(30):
        if(teams['league']['standard'][team]['tricode'] == tricode):
            return teams['league']['standard'][team]['fullName']

newlist = []
for i in teamlist:
    newlist.append(get_full_name(i))
### newlist contains all teams playing. ([0] vs [1], [2] vs [3], etc)

@app.route('/')
def main_page():
    return render_template('index.html', 
    numgames=numgames,
    team1A = newlist[0],
    team1B = newlist[1],
    team2A = newlist[2],
    team2B = newlist[3],
    time1 = timelist[0],
    time2 = timelist[1]
    )

@app.route('/Profile')
def profile_view():
    return render_template("profile.html")

@app.route('/myStats')
def stats_view():
    return render_template("myStats.html")

@app.route('/groups')
def groups_view():
    return render_template("groups.html")

#@app.route()

@app.route('/groups/create_group', methods=["GET"])
def create_group_view():
    return render_template("create_group.html")

@app.route('/groups/create_group', methods=["POST"])
def create_group_post():
    group_name = request.form.get("group_name")
    group_size = request.form.get("group_size")
    password = request.form.get("password")
    create_group(group_name, group_size, password, "chris")
    return redirect("/groups")




