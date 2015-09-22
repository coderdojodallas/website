from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64), nullable=False, index=True)
    last = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(254), nullable=False, index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.username)
