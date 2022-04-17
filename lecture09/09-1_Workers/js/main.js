var worker

function startWorker() {
    if (typeof(worker) == undefined) {
        worker = new Worker("js/worker.js")
    }
    worker.onmessage = function(event) {
        document.getElementById("result")
            .innerHTML = event.data
    }
}

function stopWorker() { 
    worker.terminate()
    worker = undefined
}
