from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'aldjkfewpeor__KK45'
db = SQLAlchemy(app)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now)
    title = db.Column('title', db.String, nullable=False)
    content = db.Column('content', db.String, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f'{self.id:>5} | {self.created.strftime("%X"):^10}| {self.title:^10} | {self.content:^20}'


db.create_all()


@app.route('/')
def index():
    posts = list(Blog.query)
    for obj in posts:
        obj.created = obj.created.strftime("%X")
    return render_template('index.html', posts=posts)


def get_post(post_id):
    post = Blog.query.filter_by(id=post_id).first()
    if not post:
        abort(404)
    return post


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            db.session.add(Blog(title, content))
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    post.created = post.created.strftime("%X")
    return render_template('post.html', post=post)


@app.route('/<int:id>/edit', methods=('get', 'post'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            edit_post = Blog.query.filter(Blog.id == id).first()
            edit_post.title = title
            edit_post.content = content
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'{post.title} was successfully deleted!')
    return redirect(url_for('index'))




