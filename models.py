from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    UniqueConstraint('city', 'state')
    venues = db.relationship('Venue', backref='city', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean, default=False)
    description = db.Column(db.String())
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable = False)
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")
    # DONE: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean, default=False)
    description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    # DONE: implement any missing fields, as a database migration using Flask-Migrate

    def __repr__(self):
        return f"<Artist {self.id} name {self.name} city state {self.city} {self.state}>"

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# insert into artists()
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    # artist = db.relationship('Artist', backref='artist', lazy=True)
    # venue = db.relationship('Venue', backref='venue', lazy=True)
