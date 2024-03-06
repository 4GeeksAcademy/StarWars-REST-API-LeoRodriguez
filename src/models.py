from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                "email": self.email}


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250))
    weight = db.Column(db.String(250))
    birth_day = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))

    def __repr__(self):
        return '<People %r>' % self.full_name

    def serialize(self):
        return {"id": self.id,
                "full_name": self.full_name}            


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    terraine = db.Column(db.String(250))
    climate = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "name": self.name}


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[user_id])
    planet = db.relationship('Planet', foreign_keys=[planet_id])
    people = db.relationship('People', foreign_keys=[people_id])

    def __repr__(self):
        return f'<Favorites {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "planet_id": self.planet_id,
                "people_id": self.people_id}