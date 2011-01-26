//global variables
var svgQsoText;

function init(evt) {
    //get reference to child (content) of the city text-Element
    svgQsoText = document.getElementById("textNode").firstChild;
}

function showQSO(evt) {
    evt.target.setAttributeNS(null,"r","8");
    evt.target.setAttributeNS(null,"opacity","0.5");
    svgQsoText.nodeValue = evt.target.getAttribute("call") + " " + evt.target.getAttribute("freq");
    //svgQsoText.nodeValue = qsotext;
}

function hideQSO(evt) {
    evt.target.setAttributeNS(null,"r","3");
    evt.target.setAttributeNS(null,"opacity","1.0");
    svgQsoText.nodeValue = " ";
}

function QSOClick(call) {
    //show an alert message
    svgQsoText.nodeValue = call;
    window.open("http://www.qrz.com/db/" + call, "QRZ Lookup");
}