function setLegs(noLegs) {
    switch(noLegs) {
        case 0:
            document.getElementById("no_legs").value = "0";

            document.getElementById("leg-0-form").style.visibility = "collapse";
            document.getElementById("leg-1-form").style.visibility = "collapse";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case 1:
            document.getElementById("no_legs").value = "1";

            document.getElementById("leg-0-form").style.visibility = "visible";
            document.getElementById("leg-1-form").style.visibility = "collapse";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case 2:
            document.getElementById("no_legs").value = "2";

            document.getElementById("leg-0-form").style.visibility = "visible";
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "collapse";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case 3:
            document.getElementById("no_legs").value = "3";

            document.getElementById("leg-0-form").style.visibility = "visible";
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "visible";
            document.getElementById("leg-3-form").style.visibility = "collapse";
            break;
        case 4:
            document.getElementById("no_legs").value = "4";

            document.getElementById("leg-0-form").style.visibility = "visible";
            document.getElementById("leg-1-form").style.visibility = "visible";
            document.getElementById("leg-2-form").style.visibility = "visible";
            document.getElementById("leg-3-form").style.visibility = "visible";
            break;
    }
}

function displayTradeLegsFromStrategy() {
    let strategy = document.getElementById("strategy").value;

    switch(strategy) {
        case "Stock":
            document.getElementById("open_underlying").setAttribute('readonly', '');
            document.getElementById("close_underlying").setAttribute('readonly', '');
            break;
        default:
            document.getElementById("open_underlying").removeAttribute('readonly');
            document.getElementById("close_underlying").removeAttribute('readonly');
            break;
    }

    switch(strategy) {
        case "Stock":
            setLegs(0);
            break;
        case "Long Call":
            setLegs(1);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";
            break;
        case "Long Put":
            setLegs(1);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "put";
            break;
        case "Covered Call":
            setLegs(1);
            document.getElementById("legs-0-opened").value = "sold";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";
            break;
        case "Cash Secured Put":
            setLegs(1);
            document.getElementById("legs-0-opened").value = "sold";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "put";
            break;
        case "Put Credit Spread":
        case "Calendar Put Spread":
            setLegs(2);
            document.getElementById("legs-0-opened").value = "sold";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "put";

            document.getElementById("legs-1-opened").value = "bought";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "put";
            break;
        case "Put Debit Spread":
            setLegs(2);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "put";

            document.getElementById("legs-1-opened").value = "sold";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "put";
            break;
        case "Call Credit Spread":
            setLegs(2);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";

            document.getElementById("legs-1-opened").value = "sold";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "call";
            break;
        case "Call Debit Spread":
        case "Calendar Call Spread":
        case "Diagonal Spread":
        case "Diagonal Spread (PMCC)":
            setLegs(2);
            document.getElementById("legs-0-opened").value = "sold";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";

            document.getElementById("legs-1-opened").value = "bought";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "call";
            break;
        case "Unbalanced Butterfly Put":
            setLegs(3);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "put";

            document.getElementById("legs-1-opened").value = "sold";
            document.getElementById("legs-1-size").value = "3";
            document.getElementById("legs-1-contract_type").value = "put";

            document.getElementById("legs-2-opened").value = "bought";
            document.getElementById("legs-2-size").value = "2";
            document.getElementById("legs-2-contract_type").value = "put";
            break;
        case "Double Calendar Spread":
            setLegs(4);
            document.getElementById("legs-0-opened").value = "sold";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";

            document.getElementById("legs-1-opened").value = "bought";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "call";

            document.getElementById("legs-2-opened").value = "sold";
            document.getElementById("legs-2-size").value = "1";
            document.getElementById("legs-2-contract_type").value = "put";

            document.getElementById("legs-3-opened").value = "bought";
            document.getElementById("legs-3-size").value = "1";
            document.getElementById("legs-3-contract_type").value = "put";
            break;
        case "Iron Condor":
            setLegs(4);
            document.getElementById("legs-0-opened").value = "bought";
            document.getElementById("legs-0-size").value = "1";
            document.getElementById("legs-0-contract_type").value = "call";

            document.getElementById("legs-1-opened").value = "sold";
            document.getElementById("legs-1-size").value = "1";
            document.getElementById("legs-1-contract_type").value = "call";

            document.getElementById("legs-2-opened").value = "sold";
            document.getElementById("legs-2-size").value = "1";
            document.getElementById("legs-2-contract_type").value = "put";

            document.getElementById("legs-3-opened").value = "bought";
            document.getElementById("legs-3-size").value = "1";
            document.getElementById("legs-3-contract_type").value = "put";
            break;
        default:
            break;
    }

}

function displayTradeLegsFromNoLegs() {
    let noLegs = document.getElementById("no_legs").value;

    setLegs(parseInt(noLegs));
}

function calcPnl() {
    let oPrem = document.getElementById("open_premium").value;
    let cPrem = document.getElementById("close_premium").value;
    let noContracts = parseInt(document.getElementById("no_contracts").value);
    let oDate = new Date(document.getElementById("open_date").value);
    let cDate = new Date(document.getElementById("close_date").value);

    console.log("calcPnl function called");
    if ((! [undefined, null, ''].includes(oPrem)) && (! [undefined, null, ''].includes(cPrem))) {
        let pnl = (parseFloat(oPrem) + parseFloat(cPrem))*noContracts;
        if(document.getElementById("strategy").value != "Stock") {
            pnl = pnl*100; // each contract corresponds to 100 shares
        }
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