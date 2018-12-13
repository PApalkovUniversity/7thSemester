import sqlite3
import os
from flask import Flask, request, g, redirect, url_for, render_template, session
from threading import Lock
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from crypto_api import get_info

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key'

# ======== crypto part =======
# async_mode = None
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock()

@socketio.on('my_event')
def test_message():
    emit('price_responce', get_info())


@app.route('/pavel/crypto')
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

# ====== notes part ======

def connect_db():
    rv = sqlite3.connect('notes.db')
    return rv

def get_db():
    #Если ещё нет соединения с базой данных, открыть новое - для
    #текущего контекста приложения
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    #Закрыть базу данных при разрыве соединения
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/pavel/notes')
def show_all_posts():
    db = get_db()
    cur = db.execute('select * from notes')
    articles = cur.fetchall()
    return render_template('post_list.html', articles=articles)


@app.route('/pavel/notes/post/<int:post_id>')
def single_post(post_id):
    db = get_db()
    cur = db.execute('select * from notes where id=?', [(post_id)])
    article = cur.fetchall()
    return render_template('post_detail.html', article=article[0])


@app.route('/pavel/notes/create')
def create_post():
    return render_template('create_post.html')


@app.route('/pavel/notes/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into notes(author, post) values (?, ?)',
                [request.form['author'], request.form['text']])
    db.commit()
    return redirect(url_for('show_all_posts'))


@app.route('/pavel/notes/delete/<int:post_id>')
def delete(post_id):
    db = get_db()
    db.execute('delete from notes where id=?', [(post_id)])
    db.commit()
    return redirect(url_for('show_all_posts'))


@app.route('/pavel/notes/rewrite/<int:post_id>')
def rewrite(post_id):
    db = get_db()
    cur = db.execute('select * from notes where id=?', [(post_id)])
    article = cur.fetchall()
    return render_template('rewrite_post.html', article=article[0])


@app.route('/pavel/notes/add_old/<int:post_id>', methods=['POST'])
def add_old(post_id):
    db = get_db()
    db.execute('update notes set author=?, post=? where id=?',
    [request.form['author'], request.form['text'], post_id])
    db.commit()
    return redirect(url_for('show_all_posts'))

# ===== standart part ========
@app.route('/pavel/home')
def show_home():
    return render_template('home.html')

@app.route('/pavel/info')
def show_info():
    return render_template('info.html')

@app.route('/pavel/photos')
def show_photo():
    return render_template('photos.html')

@app.route('/pavel/dynamic')
def show_dynamic():
    return render_template('dynamic.html')

@app.route('/pavel/banners')
def show_banners():
    return render_template('banners.html')

@app.route('/pavel/search')
def show_search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5002)
