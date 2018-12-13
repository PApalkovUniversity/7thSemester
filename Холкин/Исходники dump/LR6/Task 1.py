import sqlite3
import os
from flask import Flask, request, g, redirect, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key'


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


@app.route('/')
def show_all_posts():
    db = get_db()
    cur = db.execute('select * from notes')
    articles = cur.fetchall()
    return render_template('post_list.html', articles=articles)


@app.route('/post/<int:post_id>')
def single_post(post_id):
    db = get_db()
    cur = db.execute('select * from notes where id=?', [(post_id)])
    article = cur.fetchall()
    return render_template('post_detail.html', article=article[0])


@app.route('/create')
def create_post():
    return render_template('create_post.html')


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into notes(author, post) values (?, ?)',
                [request.form['author'], request.form['text']])
    db.commit()
    return redirect(url_for('show_all_posts'))


@app.route('/delete/<int:post_id>')
def delete(post_id):
    db = get_db()
    db.execute('delete from notes where id=?', [(post_id)])
    db.commit()
    return redirect(url_for('show_all_posts'))


@app.route('/rewrite/<int:post_id>')
def rewrite(post_id):
    db = get_db()
    cur = db.execute('select * from notes where id=?', [(post_id)])
    article = cur.fetchall()
    return render_template('rewrite_post.html', article=article[0])


@app.route('/add_old/<int:post_id>', methods=['POST'])
def add_old(post_id):
    print("IFFERFERFE", post_id)
    db = get_db()
    db.execute('update notes set author=?, post=? where id=?',
    [request.form['author'], request.form['text'], post_id])
    db.commit()
    return redirect(url_for('show_all_posts'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
