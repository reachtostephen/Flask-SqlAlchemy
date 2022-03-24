from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, InfoModel
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(os.getenv('user'), os.getenv('password'),
                                                                          os.getenv('host'), os.getenv('database'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        user = InfoModel.query.filter_by(name=name).first()
        if not user:
            new_user = InfoModel(name=name, age=age)
            db.session.add(new_user)
            db.session.commit()
        return render_template('success.html',message="Your validation is succeeded, Welcome to our site")


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        oldname = request.form['oldname']
        newname = request.form['newname']
        age = request.form['age']
        user = InfoModel.query.filter_by(name=oldname).first()
        if not user:
            return f"Name not found in our Database!"
        user.name = newname
        user.age = age
        db.session.commit()
        return render_template("success.html", message="Edit done!")
    return render_template("edit_form.html")


@app.route('/del', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        user = InfoModel.query.filter_by(name=name).first()
        if not user:
            return f"Name not found in our Database!"
        db.session.delete(user)
        db.session.commit()
        return f"You have been removed from our Database, Sad to see you leave!"
    return render_template("del_form.html")


if __name__ == '__main__':
    app.run(debug=True)
