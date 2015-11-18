from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64), nullable=False, index=True)
    last = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(254), nullable=False, index=True, unique=True)
    age_group_1 = db.Column(db.Boolean, nullable=False, index=True)
    age_group_2 = db.Column(db.Boolean, nullable=False, index=True)
    age_group_3 = db.Column(db.Boolean, nullable=False, index=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False, index=True)

    __table_args__ = (
        db.CheckConstraint('age_group_1 or age_group_2 or age_group_3',
                           name='age_group_selected'),
    )

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first, self.last, self.email)

    def __repr__(self):
        message = (
            "<models.User id={0}, first='{1}', last='{2}', email='{3}'>"
            .format(self.id, self.first, self.last, self.email)
        )
        return message
