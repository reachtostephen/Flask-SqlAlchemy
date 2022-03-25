from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InfoModel(db.Model):
    __tablename__ = 'Employee'

    name = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"{self.name}:{self.password}"
