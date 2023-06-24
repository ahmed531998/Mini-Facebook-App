from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db
from flaskblog.forms import LoginForm
from flaskblog.models import User, Post, Isrelated, Following
from flask_login import login_user, current_user, logout_user, login_required
import flask_whooshalchemy as wa
from flask_whooshalchemyplus import index_all

index_all(app)


wa.whoosh_index(app, User)


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.filter_by(userid=current_user.get_id()).all()
    return render_template('home.html', posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(screenname=form.username.data).first()
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful')
    return render_template('login.html', title='Login', form=form)


@app.route("/search")
def search():
    users = User.query.whoosh_search(request.args.get('query')).all()
    if users:
        return render_template('search.html', users=users)
    else:
        flash('No Such User!')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", defaults={'username' : ''})
@app.route("/account/<username>")
@login_required
def account(username):

    user = current_user
    if (username!=''):
        user = User.query.filter_by(screenname=username).first()


    userFans = Following.query.filter_by(userid=user.userid).all()
    fans = []
    for relation in userFans:
        fans.append(User.query.filter_by(userid=relation.followerid).first())

    marriages = []
    userMarriages = Isrelated.query.filter_by(userid=user.userid, type="marriage")
    for relation in userMarriages:
        marriages.append(User.query.filter_by(userid=relation.relateduserid).first())

    dates = []
    userDates = Isrelated.query.filter_by(userid=user.userid, type="date")
    for relation in userDates:
        dates.append(User.query.filter_by(userid=relation.relateduserid).first())

    return render_template('account.html', title='Account', user=user, fans=fans, marriages=marriages, dates=dates)

@app.route("/users/<username>")
@login_required
def users(username):
    return render_template('account.html', title='Account')
