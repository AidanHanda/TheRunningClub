import datetime

from flask_login import UserMixin

from main import db
from passlib.apps import custom_app_context as pwd_context


runs_to_runners = db.Table('runs_to_runners',
    db.Column('runs_id', db.Integer, db.ForeignKey('runs.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), index = True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    #club = db.Column(db.Integer, db.ForeignKey("clubs.id"))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return self.email

class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(db.Integer, primary_key= True)
    run_name = db.Column(db.Text)
    location = db.Column(db.Text)
    pace = db.Column(db.String(50))
    image_url = db.Column(db.String(512))
    time = db.Column(db.DateTime)
    #club = db.Column(db.Integer, db.ForeignKey("clubs.id"))

    runners = db.relationship('User', secondary=runs_to_runners)

    @staticmethod
    def clearDone():
        for run in Run.query.all():
            if run.time < datetime.datetime.now():
                db.session.delete(run)
        db.session.commit()

    def __repr__(self):
        return self.run_name

# class Club(db.Model):
#     __tablename__ = "clubs"
#
#     id = db.Column(db.Integer, primary_key= True)
#     club_name = db.Column(db.Text)
#     club_location = db.Column(db.Text)