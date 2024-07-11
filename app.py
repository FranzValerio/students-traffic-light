from flask import Flask, render_template, request, redirect, url_for, Response
from flask_socketio import SocketIO, emit
from functools import wraps
import eventlet
import eventlet.wsgi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Dictionary to keep track of students' statuses
students_status = {}

# Simple authentication
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

def check_auth(username, password):
    """Check if a username / password combination is valid."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
@requires_auth
def admin():
    return render_template('admin.html', students_status=students_status)

@socketio.on('join')
def on_join(data):
    username = data['username']
    students_status[username] = 'red'
    emit('update_status', students_status, broadcast=True)

@socketio.on('status_change')
def status_change(data):
    username = data['username']
    status = data['status']
    students_status[username] = status
    emit('update_status', students_status, broadcast=True)

@socketio.on('reset')
def reset():
    global students_status
    students_status = {key: 'red' for key in students_status.keys()}
    emit('update_status', students_status, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)