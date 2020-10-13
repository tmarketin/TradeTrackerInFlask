function toggleDisplay(id) {
    bodyId = id.replace('heading', 'body');
    currentStatus = document.getElementById(bodyId).style.display;
    if(currentStatus == "none") {
        document.getElementById(bodyId).style.display = "block";
    }
    else {
        document.getElementById(bodyId).style.display = "none";
    }
}