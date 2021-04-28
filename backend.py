# Imports the Google Cloud client library
from google.cloud import datastore
# Instantiates a client
datastore_client = datastore.Client()

def update_games():
    #get json
    import requests, json
    #get url of today's scoreboard.. easier this way than doing date stuff
    json1 = (requests.get('http://data.nba.net/10s/prod/v1/today.json')).json()
    url = (json1['links'])['currentScoreboard']
    url = 'http://data.nba.net/10s' + url

    #get json for today's scores
    json2 = (requests.get(url)).json()
    numgames = json2['numGames']    
    #loop thru games of today
    for game in json2['games']:
        if not game['isRecapArticleAvail']: # game not finished
            status = 'not_done'
            winner = 'none'
        else:
            status = 'done'
            if game['hTeam']['score'] > game['vTeam']['score']:
                winner = 'home'
            else:
                winner = 'visitor'
        #upload record to datastore
        entity_key =  datastore_client.key('game', game['gameId'])
        game_entity = datastore.Entity(key=entity_key)
        game_entity['home_team'] = game['hTeam']['triCode']
        game_entity['visitor_team'] = visitor_team = game['vTeam']['triCode']
        game_entity['status'] =  status
        game_entity['winner'] = winner
        datastore_client.put(game_entity)


def update_bets():
    #select all unfinished bets
    query = datastore_client.query(kind='bet')
    result = query.add_filter('result', '=', 'none').fetch()
    for bet in result:
        print(bet['game'])
        #find corresponding game
        game = datastore_client.get(datastore_client.key('game', bet['game']))
        print(game['status'])
        if game['status'] != 'done': break        
        #find corresp. user
        user = datastore_client.get(datastore_client.key('userCreds', bet['user']))
        print(user)
        if game['winner'] == bet['team']: #if bet wins, add 100pts to user
            bet.update({'result': 'win'.decode('utf-8')})
            oldpoints = user['points']
            user.update({'points': (oldpoints +100)})
        else:
            bet.update({'result': 'loss'.decode('utf-8')})
        datastore_client.put(bet)