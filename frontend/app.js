// const API =
// "https://f9bdmtcslf.execute-api.ap-south-1.amazonaws.com/dev/chat";

// const CLIENT_ID = "fintech";

// const messages = document.getElementById("messages");

// const input = document.getElementById("message");

// const button = document.getElementById("sendBtn");

// function addMessage(text, cls){

//     const div = document.createElement("div");

//     div.className = "message " + cls;

//     div.innerText = text;

//     messages.appendChild(div);

//     messages.scrollTop = messages.scrollHeight;

// }

// async function sendMessage(){

//     const question = input.value.trim();

//     if(question==="") return;

//     addMessage(question,"user");

//     input.value="";

//     try{

//         const response = await fetch(API,{

//             method:"POST",

//             headers:{
//                 "Content-Type":"application/json"
//             },

//             body:JSON.stringify({

//                 client_id:CLIENT_ID,

//                 message:question

//             })

//         });

//         const data = await response.json();

//         addMessage(data.answer,"bot");

//     }

//     catch(err){

//         addMessage("Unable to contact server.","bot");

//         console.error(err);

//     }

// }

// button.onclick = sendMessage;

// input.addEventListener("keypress",function(e){

//     if(e.key==="Enter"){

//         sendMessage();

//     }

// });

const API =
    "https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev/chat";

const CLIENT_ID = "fintech";

const messages = document.getElementById("messages");
const input = document.getElementById("message");
const button = document.getElementById("sendBtn");


function addMessage(text, cls) {

    const div = document.createElement("div");

    div.className = "message " + cls;

    div.innerText = text;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;
}


async function sendMessage() {

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    addMessage(question, "user");

    input.value = "";

    button.disabled = true;

    try {

        const response = await fetch(API, {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "x-api-key": "fintech-key"
            },

            body: JSON.stringify({

                client_id: CLIENT_ID,

                message: question

            })

        });


        const data = await response.json();


        if (!response.ok) {

            addMessage(
                data.error || "Request failed.",
                "bot"
            );

            return;
        }


        addMessage(
            data.answer || "No answer received.",
            "bot"
        );


    } catch (err) {

        addMessage(
            "Unable to contact server.",
            "bot"
        );

        console.error(err);

    } finally {

        button.disabled = false;

        input.focus();

    }
}


button.addEventListener("click", sendMessage);


input.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        sendMessage();

    }

});