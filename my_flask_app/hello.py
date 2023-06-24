from flask import Flask, render_template, url_for, flash, redirect, request
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, current_user, logout_user, login_required, LoginManager

import psycopg2
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahmed:123456@localhost/test'

db = SQLAlchemy(app)

login_manager = LoginManager()
from models import *

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

posts = []

db.create_all()
db.session.commit()



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/login", methods=['GET','POST'])
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
            flash('FAILURE!')
    
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


if __name__ == '__main__':
    app.run(debug=True)
