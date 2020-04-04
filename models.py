from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    access_token = db.Column(db.String(100))
    password = db.Column(db.String(100))
    uid = db.Column(db.Integer)
    openid = db.Column(db.Integer)
    refresh_token = db.Column(db.String(100))
    scope = db.Column(db.String(100))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username
