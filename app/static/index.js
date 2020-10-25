function toggleDisplay(id) {
    let bodyId = id.replace('heading', 'body');
    let currentStatus = document.getElementById(bodyId).style.display;
    if(currentStatus == "none") {
        document.getElementById(bodyId).style.display = "block";
    }
    else {
        document.getElementById(bodyId).style.display = "none";
    }
}

function filterAllTrades() {
    document.getElementById("filterButtonAll").classList.add("active");
    document.getElementById("filterButtonOpen").classList.remove("active");
    document.getElementById("filterButtonWins").classList.remove("active");
    document.getElementById("filterButtonLosses").classList.remove("active");

    let openTrades = document.getElementsByClassName("panel-warning");
    let winningTrades = document.getElementsByClassName("panel-success");
    let losingTrades = document.getElementsByClassName("panel-danger");

    let idx;
    // make open trades visible
    for(idx = 0; idx < openTrades.length; idx++) {
        openTrades[idx].style.display = "block";
    }
    // make winning trades visible
    for(idx = 0; idx < winningTrades.length; idx++) {
        winningTrades[idx].style.display = "block";
    }
    // make losing trades visible
    for(idx = 0; idx < losingTrades.length; idx++) {
        losingTrades[idx].style.display = "block";
    }
}

function filterOpenTrades() {
    document.getElementById("filterButtonAll").classList.remove("active");
    document.getElementById("filterButtonOpen").classList.add("active");
    document.getElementById("filterButtonWins").classList.remove("active");
    document.getElementById("filterButtonLosses").classList.remove("active");

    let openTrades = document.getElementsByClassName("panel-warning");
    let winningTrades = document.getElementsByClassName("panel-success");
    let losingTrades = document.getElementsByClassName("panel-danger");

    let idx;
    // make open trades visible
    for(idx = 0; idx < openTrades.length; idx++) {
        openTrades[idx].style.display = "block";
    }
    // make winning trades not visible
    for(idx = 0; idx < winningTrades.length; idx++) {
        winningTrades[idx].style.display = "none";
    }
    // make losing trades not visible
    for(idx = 0; idx < losingTrades.length; idx++) {
        losingTrades[idx].style.display = "none";
    }
}

function filterWinningTrades() {
    document.getElementById("filterButtonAll").classList.remove("active");
    document.getElementById("filterButtonOpen").classList.remove("active");
    document.getElementById("filterButtonWins").classList.add("active");
    document.getElementById("filterButtonLosses").classList.remove("active");

    let openTrades = document.getElementsByClassName("panel-warning");
    let winningTrades = document.getElementsByClassName("panel-success");
    let losingTrades = document.getElementsByClassName("panel-danger");

    let idx;
    // make open trades visible
    for(idx = 0; idx < openTrades.length; idx++) {
        openTrades[idx].style.display = "none";
    }
    // make winning trades not visible
    for(idx = 0; idx < winningTrades.length; idx++) {
        winningTrades[idx].style.display = "block";
    }
    // make losing trades not visible
    for(idx = 0; idx < losingTrades.length; idx++) {
        losingTrades[idx].style.display = "none";
    }
}

function filterLosingTrades() {
    document.getElementById("filterButtonAll").classList.remove("active");
    document.getElementById("filterButtonOpen").classList.remove("active");
    document.getElementById("filterButtonWins").classList.remove("active");
    document.getElementById("filterButtonLosses").classList.add("active");

    let openTrades = document.getElementsByClassName("panel-warning");
    let winningTrades = document.getElementsByClassName("panel-success");
    let losingTrades = document.getElementsByClassName("panel-danger");

    let idx;
    // make open trades visible
    for(idx = 0; idx < openTrades.length; idx++) {
        openTrades[idx].style.display = "none";
    }
    // make winning trades not visible
    for(idx = 0; idx < winningTrades.length; idx++) {
        winningTrades[idx].style.display = "none";
    }
    // make losing trades not visible
    for(idx = 0; idx < losingTrades.length; idx++) {
        losingTrades[idx].style.display = "block";
    }
}