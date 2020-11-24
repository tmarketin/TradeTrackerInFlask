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
    // make open trades not visible
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

function setFilterValue(btnId, value) {
    document.getElementById(btnId).getElementsByTagName("span")[0].innerHTML = value;
    filterContent()
}

function resetFilters() {
    let idList = ["btn-filter-status", "btn-filter-strategy", "btn-filter-ticker", "btn-filter-year"];

    for(let id of idList) {
        document.getElementById(id).getElementsByTagName("span")[0].innerHTML = "All";
    }
    filterContent();
}

function filterContent() {
    let idStatus = "btn-filter-status";
    let idStrategy = "btn-filter-strategy";
    let idTicker = "btn-filter-ticker";
    let idYear = "btn-filter-year";

    let filterStatusValue = document.getElementById(idStatus).getElementsByTagName("span")[0].innerHTML;
    let filterStatusClassMap = new Map();
    filterStatusClassMap.set('All', 'panel');
    filterStatusClassMap.set('Open', 'panel-warning');
    filterStatusClassMap.set('Wins', 'panel-success');
    filterStatusClassMap.set('Losses', 'panel-danger');

    let filterStrategyValue = document.getElementById(idStrategy).getElementsByTagName("span")[0].innerHTML;
    let filterTickerValue = document.getElementById(idTicker).getElementsByTagName("span")[0].innerHTML;
    let filterYearValue = document.getElementById(idYear).getElementsByTagName("span")[0].innerHTML;

    let tradesList = document.getElementsByClassName("panel");
    for(let idx = 0; idx < tradesList.length; idx++) {
        let isStatusFilterOk = tradesList[idx].classList.contains(filterStatusClassMap.get(filterStatusValue));
        let isStrategyFilterOk = (tradesList[idx].getElementsByClassName("panel-heading-strategy")[0].innerHTML == filterStrategyValue)
                                || (filterStrategyValue == "All");
        let isTickerFilterOk = (tradesList[idx].getElementsByClassName("panel-heading-ticker")[0].innerHTML == filterTickerValue)
                                || (filterTickerValue == "All");

        let oDate = new Date(tradesList[idx].getElementsByClassName("panel-body-open-date")[0].innerHTML);
        let isYearFilterOk = (oDate.getFullYear() == filterYearValue) || (filterYearValue == "All");
        
        if (isStatusFilterOk && isStrategyFilterOk && isTickerFilterOk && isYearFilterOk) {
            tradesList[idx].style.display = "block";
        }
        else {
            tradesList[idx].style.display = "none";
        }
    }
}