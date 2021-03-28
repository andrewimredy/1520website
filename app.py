from flask import Flask, render_template, session

from google.cloud import datastore
from auth import blue as auth_blueprint

from user import userStore, generate_creds, hash_password

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

app.register_blueprint(auth_blueprint, url_prefix="/auth")

datastore_client = datastore.Client()
userstore = userStore(datastore_client)

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
    user = get_user()
    return render_template('index.html', user=user,
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
    user = get_user()
    points = get_points(user)
    return render_template("myStats.html" , user=user , points=points)

@app.route('/groups')
def groups_view():
    return render_template("groups.html")

@app.route('/login')
def login():
    return render_template("login.html")

def get_user():
    return session.get("user", None)

def get_points(userStr):
    user_key = userstore.ds.key("userCreds", userStr)
    user = userstore.ds.get(user_key)
    return user["points"]