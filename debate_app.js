var connectBt = document.getElementById("connectBut")
var disconnectBt = document.getElementById("disconnectBut")

var urlBox = document.getElementById("wsUrl")
var connectionStatusIndicator = document.getElementById("connection-status")

var conversationBox = document.getElementById("conversation-box")
var conversation = document.getElementById("conversation")
var sendMessageBox = document.getElementById("sendMessage")
var sendMessageBt = document.getElementById("sendMessageBut")

sendMessageBt.onclick = function{
    var message = sendMessageBox.value
    if (message!='' || message!=null){
        sendMessage(message)
    }else{
        alert("Please enter a query in the box!")
    } 
}

function sendMessage(message){
    //TODO:Send the obtained message to the url
    addSendMessageBox()
}

function addSendMessageBox(message){

}

function addMessageReceivedBox(message){
    //Call when a message is received from the server
}