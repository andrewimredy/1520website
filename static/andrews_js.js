function placeBet(teamAndGame){   
    //gameId comes in as 'x000000000' to show bet pref and id. lets parse it
    let team = teamAndGame[0];
    let gameId = teamAndGame.substring(1);

    //if no user is logged in, alert
    let usernameBox =  document.getElementById('username')
    if(usernameBox  === null){
        alert('Please log in to place bets!');
        return;
    }
    //graphical changes
    changeBetBox(gameId, team);
    //send post request to backend
    var req = new XMLHttpRequest();
    req.open('POST', '/bet' + '/' + gameId + '/' + team);
    req.send();
    //put record into local storage (for refresh guard...)
    localStorage.setItem(gameId, team);
    return;
}

//highlights team that you bet on, disappears bet buttons
function changeBetBox(gameId, team){
//change time heading to "Bet Placed", highlight team
    document.getElementById('t' + gameId).innerHTML = 'Bet Placed';
    if(team === 'v'){
        document.getElementById('a' + gameId).style = 'border-style: solid; border-width: medium; border-radius: 10px;';
    }else{
        document.getElementById('b' + gameId).style = 'border-style: solid; border-width: medium; border-radius: 10px;';
    }
    //hide buttons
    document.getElementById('v' + gameId).style = 'display: none;';
    document.getElementById('h' + gameId).style = 'display: none;';
    return;
}

//changes bet box for bets already placed..
window.onload = function showPrevBets(){
    let gameBlocks = document.getElementsByClassName('game_block');
    if(document.getElementById('username')){    
        for (i = 0; i < gameBlocks.length; i++){
            let id = gameBlocks[i].getElementsByClassName('game_time')[0].getElementsByClassName('game_block_time')[0].id
            id = id.substring(1)
            let betTeam = localStorage.getItem(id);
            if(betTeam){
                changeBetBox(id, betTeam);
            }        
        }  
    } 
    return; 
}