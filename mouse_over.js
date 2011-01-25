//global variables
var svgQsoText;

function init(evt) {
    //get reference to child (content) of the city text-Element
    svgQsoText = document.getElementById("textNode").firstChild;
}

function showQSO(city) {
    //change text-Value
    svgQsoText.nodeValue = city;
}

function hideQSO() {
    //empty text-String
    svgQsoText.nodeValue = " ";
}

function QSOClick(call) {
    //show an alert message
    svgQsoText.nodeValue = call;
    window.open("http://www.qrz.com/db/" + call, "QRZ Lookup");
}