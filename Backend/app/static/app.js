var coll = document.getElementsByClassName("collapsible")

for(let i=0;i<coll.length;i++){
    coll[i].addEventListener("click",function(){
        this.classList.toggle("active");
        var content = this.nextElementSibling;

        if(content.style.maxHeight){
            content.style.maxHeight = null;

        }else{
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
}

class Chatbox{
    constructor(){
        this.args = {
            openButton : document.querySelector('.chatbox_button'),
            chatBox : document.querySelector('.chatbox_support'),
            sendButton : document.querySelector('.send_button')

        }
        this.state = false;
        this.messages = [];
        
    }
}