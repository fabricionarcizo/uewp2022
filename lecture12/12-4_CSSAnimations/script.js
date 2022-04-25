function listener(event) {
    switch(event.type) {
        case "animationstart":
            console.log(`Started: elapsed time is ${event.elapsedTime}`);
            break;
        case "animationend":
            console.log(`Ended: elapsed time is ${event.elapsedTime}`);
            break;
        case "animationiteration":
            console.log(`New loop started at time ${event.elapsedTime}`);
            break;
    }
}

var element = document.getElementById("element");
element.addEventListener("animationstart", listener, false);
element.addEventListener("animationend", listener, false);
element.addEventListener("animationiteration", listener, false);

element.className = "stretch";