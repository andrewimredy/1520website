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

    #if already exists, don't create again TODO
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
        print(kind, id, home_team, visitor_team, status, winner)
        #upload record to datastore
        entity_key =  datastore_client.key('game', game['gameId'])
        game_entity = datastore.Entity(key=entity_key)
        game_entity['home_team'] = game['hTeam']['triCode']
        game_entity['visitor_team'] = visitor_team = game['vTeam']['triCode']
        game_entity['status'] =  status
        game_entity['winner'] = winner
        datastore_client.put(game_entity)

update_games()