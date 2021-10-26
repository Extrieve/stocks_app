from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return 'Name %r' % self.id
