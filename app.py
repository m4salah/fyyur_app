#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from enum import unique
import json
from operator import ge
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)

from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
import datetime
from models import db, Venue, Show, Artist, City

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    cities = City.query.order_by('id').all()
    return render_template('pages/venues.html', areas=cities)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    name = request.form.get('search_term')
    venues = Venue.query.filter(Venue.name.ilike('%' + name + '%'))
    count = len(venues.all())
    return render_template('pages/search_venues.html', results=venues, count=count, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    # upcoming_shows = Show.query.filter(Show.start_date > ct , Show.venue_id == venue_id).all()
    # past_shows = Show.query.filter(Show.start_date < ct , Show.venue_id == venue_id).all()

    past_shows = []
    upcoming_shows = []
    ct = datetime.datetime.now()

    venue = Venue.query.get_or_404(venue_id)

    for show in venue.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_date': show.start_date.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_date <= ct:
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    data = vars(venue)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html',
                            data=data,
                            venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    error = False

    form = VenueForm(request.form)

    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_talent = request.form.get("seeking_talent") != None
    seeking_description = form.seeking_description.data

    city_object = City()
    city_result = City.query.filter_by(city=city, state=state)

    if len(city_result.all()) == 0:
        print(city_result.all())
        city_object = City(city=city, state=state)
    else:
        print(city_result.first())
        city_object = city_result.first()

    venue = Venue(
        name=name,
        phone=phone,
        address=address,
        genres=genres,
        image_link=image_link,
        facebook_link=facebook_link,
        website_link=website_link,
        looking_for_talent=bool(seeking_talent),
        description=seeking_description
    )
    venue.city = city_object

    try:
        db.session.add(city_object)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    # on successful db insert, flash success

    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    else:
        flash('Venue ' + request.form['name'] + ' could not be listed.')
        return redirect(url_for('create_venue_form'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    data = Artist.query.order_by('id').all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    name = request.form.get('search_term')
    artists = Artist.query.filter(Artist.name.ilike('%' + name + '%'))
    count = len(artists.all())
    return render_template('pages/search_artists.html', results=artists, count=count, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # DONE: replace with real artist data from the artist table, using artist_id
    ct = datetime.datetime.now()
    past_shows = []
    upcoming_shows = []

    artist = Artist.query.get_or_404(artist_id)

    for show in artist.shows:
        temp_show = {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_date': show.start_date.strftime("%m/%d/%Y, %H:%M")
        }

        if show.start_date <= ct:
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    data = vars(artist)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
    return render_template('pages/show_artist.html',
                            data=data,
                            artist=artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.get(artist_id)
    # DONE: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    artist = Artist.query.get(artist_id)

    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website_link = request.form['website_link']
    artist.looking_for_venues = request.form.get("seeking_venue") != None
    artist.description = request.form['seeking_description']
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_to_edit = Venue.query.get(venue_id)
    # DONE: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue_to_edit)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city.city = request.form['city']
    venue.city.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website_link = request.form['website_link']
    venue.looking_for_talent = request.form.get("seeking_talent") != None
    venue.description = request.form['seeking_description']
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    error = False

    form = ArtistForm(request.form)

    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_venue = request.form.get("seeking_venue") != None
    seeking_description = form.seeking_description.data


    artist = Artist(
        name=name,
        city=city,
        state=state,
        phone=phone,
        genres=genres,
        image_link=image_link,
        facebook_link=facebook_link,
        website_link=website_link,
        looking_for_venues=seeking_venue,
        description=seeking_description
    )
    try:
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    # on successful db insert, flash success

    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    else:
        flash('Artist ' + request.form['name'] + ' could not be listed.')
        return redirect(url_for('create_artist_form'))

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.order_by('id').all()
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead
    # on successful db insert, flash success
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_date = request.form.get('start_time')

    error = False

    show = Show(
        artist_id=artist_id,
        venue_id=venue_id,
        start_date=start_date
    )

    try:
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    else:
        flash('Show could not be listed.')
        return redirect(url_for('create_show_submission'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
