
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

//changes bet box for 
function showPrevBets(){

}