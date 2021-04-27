var leaderBoardList;
var numberOfGroups;
var sortedByName = false;
var sortedByPoints = true;
var asc = true;
var globalTest;

window.onload = function() {
    /*
    const form = document.getElementById("question-form");
    form.addEventListener("submit", submitQuestion);
    loadQuestions();
    */
    console.log("Hello");
    // executes function every x milliseconds
    //window.setInterval(loadQuestions, 30000);
}

function ascendSortUsernames(){
    
}

// First index is the group. Second Index is the member. Third is [0] = username, [1] = points
function storeList(data, numGroups){
    var newList = JSON.parse(data);
    numberOfGroups = numGroups;
    //console.log(newList[0][0][0]);
    leaderBoardList = newList;
    console.log(leaderBoardList[0].length);
    return newList;
}

function highlighUser(username){
    document.querySelectorAll
}

function createLeaderboard(groupNumber){
    for(var i = 0; i < leaderBoardList[groupNumber].length; i++){
        var rowElement = document.querySelector('.row_'+ groupNumber + '_' + i);
        rowElement.innerHTML = '<div class="name">'+ leaderBoardList[groupNumber][i][0] + '</div><div class="score">'+ leaderBoardList[groupNumber][i][1] +'</div>'
    }
}

function renderAllLeaderBoards(numberOfGroups){
    for(var i = 0; i < numberOfGroups; i++){
        createLeaderboard(i);
    }
}



function ascSortByPoints(groupNumber){
    leaderBoardList[groupNumber].sort(function(a,b){
        if(a[1] > b[1]){
            return -1;
        }else{
            return 1;
        }
    });
    sortedByPoints = true;
    sortedByName = false;
    asc = true;    
    renderAllLeaderBoards(numberOfGroups);
}

function ascSortByName(groupNumber){
    console.log("ascSortByName called");
    leaderBoardList[groupNumber].sort(function(a,b){
        var aVal = a[0].toUpperCase();
        var bVal = b[0].toUpperCase();        
        if(aVal < bVal){
            return -1;
        }else{
            return 1;
        }
    });
    sortedByPoints = false;
    sortedByName = true;
    asc = true;
    renderAllLeaderBoards(numberOfGroups);
}

function descSortByPoints(groupNumber){
    leaderBoardList[groupNumber].sort(function(a,b){
        if(a[1] < b[1]){
            return -1;
        }else{
            return 1;
        }
    });
    sortedByPoints = true;
    sortedByName = false;
    asc = false;
    renderAllLeaderBoards(numberOfGroups);
}

function descSortByName(groupNumber){
    console.log("descSortByName called");
    leaderBoardList[groupNumber].sort(function(a,b){
        var aVal = a[0].toUpperCase();
        var bVal = b[0].toUpperCase();
        if(aVal > bVal){
            return -1;
        }else{
            return 1;
        }
    });
    sortedByPoints = false;
    sortedByName = true;
    asc = false;
    renderAllLeaderBoards(numberOfGroups);
}

function addEventListeners(numberOfGroups){
    console.log("Adding Event Listeners");
    var username = document.querySelector('.name_header_1');
    console.log(username);    
    // username.addEventListener("click", function() {
    // ascSortByName(1);
    // });//ascSortByName(1));
    // username.addEventListener("mouseover", function() {
    // descSortByName(1);
    // });   
    for(var i = 0; i < numberOfGroups; i++){
        var username = document.querySelector('.name_header_' + i);
        var points = document.querySelector('.score_header_' + i);
        globalTest = i;
        username.addEventListener("click", function() {
            if(sortedByPoints){
                ascSortByName(globalTest);
            }else if(asc){
                descSortByName(globalTest);
            } else{
                ascSortByName(globalTest);
            }
        });
        points.addEventListener("click", function() {
            if(sortedByName){
                ascSortByPoints(globalTest);
            }else if(asc){
                descSortByPoints(globalTest);
            } else{
                ascSortByPoints(globalTest);
            }
        });          
    }
}



