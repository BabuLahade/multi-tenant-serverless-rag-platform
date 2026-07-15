const API =
"https://f9bdmtcslf.execute-api.ap-south-1.amazonaws.com/dev/chat";

const CLIENT_ID = "fintech";

const messages = document.getElementById("messages");

const input = document.getElementById("message");

const button = document.getElementById("sendBtn");

function addMessage(text, cls){

    const div = document.createElement("div");

    div.className = "message " + cls;

    div.innerText = text;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;

}

async function sendMessage(){

    const question = input.value.trim();

    if(question==="") return;

    addMessage(question,"user");

    input.value="";

    try{

        const response = await fetch(API,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                client_id:CLIENT_ID,

                message:question

            })

        });

        const data = await response.json();

        addMessage(data.answer,"bot");

    }

    catch(err){

        addMessage("Unable to contact server.","bot");

        console.error(err);

    }

}

button.onclick = sendMessage;

input.addEventListener("keypress",function(e){

    if(e.key==="Enter"){

        sendMessage();

    }

});