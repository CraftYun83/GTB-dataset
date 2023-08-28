var fs = require('fs');
const ChatMessage = require('prismarine-chat')("1.8")

var building = false;
var d = [];
const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function callback(err) {
  if (err) throw err;
    console.log('complete');
}

function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

exports.upstreamHandler = function (meta, data, server, client) {
  /* if (meta.name === 'chat') {
    data.message = 'modified'
  } */
  server.sendPacket(meta, data)
}

// Handles packets going from the server to the client
exports.downstreamHandler = function (meta, data, server, client) {
  if (building && meta.name === "block_change") {
    d.push({"meta": meta, "data": data});
  }
  if (meta.name === "chat") {
    var chat = new ChatMessage(data);
    console.log(chat.toAnsi())
    if (data["message"].includes("The theme was: ")) {
      console.log("round finished")
      building = false;
      var fileName = generateString(10);
      fs.writeFile("gtb/"+fileName+'.json', JSON.stringify(d), 'utf8', callback);
      console.log("Saved build as "+fileName+".json")
      d = []
    } if (data["message"].includes("Round: ")) {
      console.log("round started")
      building = true;
    }
  }
  client.sendPacket(meta, data)
}