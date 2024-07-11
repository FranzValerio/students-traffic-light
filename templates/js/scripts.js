var socket = io();
var username = '';

function join() {
    username = document.getElementById('username').value;
    if (username) {
        socket.emit('join', { username: username });
        document.getElementById('login').style.display = 'none';
        document.getElementById('controls').style.display = 'block';
    }
}

function changeStatus(status) {
    socket.emit('status_change', { username: username, status: status });
}

socket.on('update_status', function(data) {
    var statusList = document.getElementById('status_list');
    statusList.innerHTML = '';
    for (var user in data) {
        var color = data[user] === 'green' ? 'green' : 'red';
        var statusText = data[user] === 'green' ? 'Estoy listo' : 'Aún no estoy listo';
        statusList.innerHTML += '<p>' + user + ': <span style="color:' + color + ';">' + statusText + '</span></p>';
    }
});