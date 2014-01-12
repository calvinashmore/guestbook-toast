import datetime

from flask import Flask, flash, redirect, render_template, request, session
import uuid


app = Flask(__name__)

class Post:
    def __init__(self, entry, name, date):
        self._entry = entry
        self._name = name
        self._date = date
        # use UUIDs to prevent collisions when deleting posts.
        self._id = str(uuid.uuid1())

    @property
    def entry(self):
        return self._entry

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def id(self):
        return self._id


# post data
# TODO(kailys): make persistent
posts = []


@app.route('/')
def index():
    return render_template(
        'index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    if not request.form['name']:
        flash("you must provide a name!")
        return redirect('/')
    posts.append(Post(
            request.form['entry'] or '<blank>',
            request.form['name'],
            datetime.datetime.now()))
    return redirect('/')

@app.route('/admin')
def admin_login():
    return render_template('login.html')

#TODO(kailys): replace with better authentication
@app.route('/admin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return admin_login()

@app.route('/moderate', methods=['POST'])
def moderate_posts():
    post_ids_to_delete = filter(lambda key: key[0], request.form)
    posts_to_delete = filter(lambda post: post.id in post_ids_to_delete, posts)
    for post in posts_to_delete:
        posts.remove(post)
    return redirect('/')


if __name__ == '__main__':
    import os
    app.secret_key = os.urandom(12)
    app.run(debug=True)
