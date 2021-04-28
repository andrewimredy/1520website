

function placeBet(teamAndGame){    
    //gameId comes in as 'x000000000' to show bet pref and id. lets parse it
    let team = teamAndGame[0];
    let gameId = teamAndGame.substring(1);

    //if no user is logged in, alert
    if(document.getElementById('username') === null){
        alert('Please log in to place bets!');
        return;
    }
    //change time heading to "Bet Placed", highlight team
    alert('t' + gameId)
    document.getElementById('t' + gameId).innerHTML = 'Bet Placed';
    if(team === 'v'){
        document.getElementById('a' + gameId).style = 'border-style: ridge; border-radius 10px';
    }else{
        document.getElementById('b' + gameId).style = 'border-style: ';
    }
}