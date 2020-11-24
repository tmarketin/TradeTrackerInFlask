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
    let visibleStrategyList = ["All"];
    let visibleTickerList = ["All"];
    let visibleYearList = ["All"];
    for(let trade of tradesList) {
        let isStatusFilterOk = trade.classList.contains(filterStatusClassMap.get(filterStatusValue));
        let isStrategyFilterOk = (trade.getElementsByClassName("panel-heading-strategy")[0].innerHTML == filterStrategyValue)
                                || (filterStrategyValue == "All");
        let isTickerFilterOk = (trade.getElementsByClassName("panel-heading-ticker")[0].innerHTML == filterTickerValue)
                                || (filterTickerValue == "All");

        let oDate = new Date(trade.getElementsByClassName("panel-body-open-date")[0].innerHTML);
        let isYearFilterOk = (oDate.getFullYear() == filterYearValue) || (filterYearValue == "All");
        
        if (isStatusFilterOk && isStrategyFilterOk && isTickerFilterOk && isYearFilterOk) {
            trade.style.display = "block";
            let strat = trade.getElementsByClassName("panel-heading-strategy")[0].innerHTML;
            if(! visibleStrategyList.includes(strat)) {
                visibleStrategyList.push(strat);
            }

            let ticker = trade.getElementsByClassName("panel-heading-ticker")[0].innerHTML;
            if(! visibleTickerList.includes(ticker)) {
                visibleTickerList.push(ticker);
            }

            let year = oDate.getFullYear();
            if(! visibleYearList.includes(year)) {
                visibleYearList.push(year);
            }
            
        }
        else {
            trade.style.display = "none";
        }
    }

    filterButtonOptions(visibleStrategyList, "button-filter-strategy-option");
    filterButtonOptions(visibleTickerList, "button-filter-ticker-option");
    filterButtonOptions(visibleYearList, "button-filter-year-option");
}

function filterButtonOptions(visibleStrategyList, optionClass) {
    let buttonStrategyOptions = document.getElementsByClassName(optionClass);
    for(let option of buttonStrategyOptions) {
        if(visibleStrategyList.includes(option.innerHTML)) {
            option.style.display = "block";
        }
        else {
            option.style.display = "none";
        }
    }
}