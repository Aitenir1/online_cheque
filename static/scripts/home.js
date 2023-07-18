const socket = new WebSocket('ws://127.0.0.1:8000/ws')

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        message: 'Hello, world'
    }));
};

socket.onmessage = function(event) {
    console.log("Message received")
    try {
        console.log(JSON.parse(event.data));
    } catch (e) {
        console.log('Error:', e.message);
    }
}
