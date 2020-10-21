function displayTradeLegsFromStrategy() {
    let strategy = document.getElementById("strategy").value;

    document.getElementById("leg-0-form").style.visibility = "visible";
    switch(strategy) {
        case "Long Call":
        case "Long Put":
        case "Covered Call":
        case "Cash Secured Put":
            document.getElementById("no_legs").value = "1";

            document.getElementById("leg-1-form").style.visibility = "collapse";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case "Put Credit Spread":
        case "Put Debit Spread":
        case "Call Credit Spread":
        case "Call Debit Spread":
        case "Calendar Call Spread":
        case "Calendar Put Spread":
        case "Diagonal Spread":
        case "Diagonal Spread (PMCC)":
            document.getElementById("no_legs").value = 2;

            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case "Double Calendar Spread":
            document.getElementById("no_legs").value = 4;

            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "visible";
            document.getElementById("leg-3-form").style.visibility = "visible";

            break;
        default:
            break;
    }

}

function displayTradeLegsFromNoLegs() {
    let noLegs = document.getElementById("no_legs").value;

    document.getElementById("leg-0-form").style.visibility = "visible";
    switch(noLegs) {
        case "1":
            document.getElementById("leg-1-form").style.visibility = "collapse";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case "2":
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case "3":
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "visible";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case "4":
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "visible";
            document.getElementById("leg-3-form").style.visibility = "visible";
            break;
    }
}

function calcPnl() {
    let oPrem = document.getElementById("open_premium").value;
    let cPrem = document.getElementById("close_premium").value;
    let oDate = new Date(document.getElementById("open_date").value);
    let cDate = new Date(document.getElementById("close_date").value);

    console.log("calcPnl function called");
    if ((! [undefined, null, ''].includes(oPrem)) && (! [undefined, null, ''].includes(cPrem))) {
        let pnl = parseFloat(oPrem) + parseFloat(cPrem);
        document.getElementById('pnl').value = pnl.toFixed(2);

        console.log("odate: " + oDate);
        console.log("cdate: " + cDate);
        if ((! [undefined, null, ''].includes(oDate)) && (! [undefined, null, ''].includes(cDate))) {
            let dateDiffMs = cDate - oDate;
            console.log("diff: " + dateDiffMs);
            if (dateDiffMs >= 0) {
                dateDiffDay = Math.ceil(dateDiffMs/(1000*60*60*24));
                console.log("Difference in days: " + dateDiffDay);
                if(dateDiffDay == 0) {
                    dateDiffDay = 1;
                }
                document.getElementById('dailypnl').value = (pnl/dateDiffDay).toFixed(2);
            }
            else {
                document.getElementById('dailypnl').value = '';
            }
        }
        else {
            document.getElementById('dailypnl').value = '';
        }
    }
    else {
        document.getElementById('pnl').value = '';
    }
}