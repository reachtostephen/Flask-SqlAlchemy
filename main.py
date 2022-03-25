import logging

from flask import Flask, render_template, request, url_for, redirect, session
from flask_migrate import Migrate
from models import db, InfoModel
from dotenv import load_dotenv

import os

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(os.getenv('user'), os.getenv('password'),
                                                                          os.getenv('host'), os.getenv('database'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
db.init_app(app)
migrate = Migrate(app, db)


def checkuser(func):
    def inner():
        name = request.form['name'].strip()
        password = request.form['password']
        user = InfoModel.query.filter_by(name=name).first()
        try:
            if user.name == name and user.password == password:
                return func(name)
        except Exception as e:
            logging.info("You are not yet registered with us!", e)
            session['message'] = 'We think You are a new User!, Please register'
            return redirect(url_for('register'))

    return inner


@app.route('/')
def form():
    return render_template("form.html")


@app.route('/login', methods=['POST'])
@checkuser
def login(name):
    if request.method == 'POST':
        message = 'Welcome ' + name
        session['message'] = message
        return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        password = request.form['password']
        new_user = InfoModel(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        message = 'Welcome ' + name
        session['message'] = message
        return redirect(url_for('home'))
    message = session['message']
    return render_template("register_form.html", message=message)


@app.route('/home')
def home():
    message = session['message']
    return render_template("success.html", message=message)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        name = request.form['name'].strip()
        user = InfoModel.query.filter_by(name=name).first()
        if not user:
            return render_template("edit_form.html", message="Wrong user")
        if user.password != request.form['oldpw']:
            return render_template("edit_form.html", message="Wrong password")
        if user.password == request.form['oldpw']:
            user.name = name
            user.password = request.form['newpw']
            db.session.commit()
        return render_template("success.html", message="Edit done!")
    return render_template("edit_form.html")


@app.route('/del', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        user = InfoModel.query.filter_by(name=name).first()
        if not user:
            return render_template("del_form.html", message="Wrong user")
        if user.password != request.form['pw']:
            return render_template("edit_form.html", message="Wrong password")
        db.session.delete(user)
        db.session.commit()
        return f"You have been removed from our Database, Sad to see you leave!"
    return render_template("del_form.html")


if __name__ == '__main__':
    app.run(debug=True)
