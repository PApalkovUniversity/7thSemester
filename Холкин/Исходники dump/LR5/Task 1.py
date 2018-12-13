from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from crypto_api import get_info

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@socketio.on('my_event')
def test_message():
    emit('price_responce', get_info())


@app.route('/')
def index():
    return render_template('price.html', async_mode=socketio.async_mode)


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(5)
        socketio.emit('price_responce', get_info())



@socketio.on('connect')
def test_connect():
    emit('price_responce', get_info())
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)




if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5003)
