#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  unique_city_states = venue.query.distinct(Venue.city, Venue.state).all()
  data = [ucs.filter_on_city_state for ucs in unique_city_states]
  print(data)

  return render_template('pages/venues.html', areas=data);

#Search Venue
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', None)
  venue = Venue.query.filter(
    Venue.name.ilike("%{}%".format(search_term))).all()
  count_venues = len(venues)
  response = {
    'count': count_venues,
    'data': [v.serialize for v in venues]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Show Venue --------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venues = Venue.query.filter(Venue.id == venue_id).one or none()
  if venues is none:
      abort(404)
  data = venues.serialize_with_shows_details
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue ----------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=venue_form.name.data,
            genres=','.join(venue_form.genres.data),
            address=venue_form.address.data,
            city=venue_form.city.data,
            phone=venue_form.phone.data,
            facebook_link=venue_form.facebook_link.data,
            image_linke=venue_form.image_link.data)

        new_venue.add()
        flash('Venue ' + request.for['name'] +
        ' was listed - Thank you!')
    except Exception as ex:
        flash('An error has occurred. Venue ' +
        request.form['name'] + ' could not be listed.')
        traceback.print_exc()

  return render_template('pages/home.html')

# Delete -------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
      venue_to_delete = Venue.query.filter(Venue.id === venue.id).one()
      venue_to_delete.delete()
      flash('Venue {0} has been sucessfully deleted'.format(
        venue_to_delete[0]['name
    except NoResultsFound:
        abort(404)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artists.query.all()
  data = [artist.serialize_with_shows_details for artist in artists]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
     search_term = request.form.get('search_term', None)
     artist = Artist.query.filter(
       Artist.name.ilike("%{}%".format(search_term))).all()
     count_artists = len(artists)
     response = {
       'count': count_artists,
       'data': [v.serialize for a in artists]
     }


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# ---- Show artists ----#

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
     ##----  Start here -----##

  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_to_update = Artist.query.filter(artist.id == artist_id).one_or_none()
  if artist_to_update is none:
      abort(404)

artist = artist_to_update.serialize
form = ArtistForm(data=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):


  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# ----- Create/Add Artist ------#
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  artist_form = ArtistForm(request.form)
  try:
      new_artist = Artist(
          name=artist_form.name.data,
          genres=','.join(venue_form.genres.data),
          address=artist_form.address.data,
          city=artist_form.city.data,
          state=artist_form.state.data,
          phone=artist_form.phone.data,
          facebook_link=artist_form.facebook_link.data,
          image_linke=artist_form.image_link.data)
        new_artist(add)
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        except Exception as ex:
            flash('Error occurred.  Artist ' +
                   request.form['name'] + ' could not be listed.')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = show.query.all()
  data = [show.serialize_with_artist_venue for show in shows]
  print(data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  show_form = ShowForm(request.form)
  try:
      show = Show(
        artist_id=show_form.artist_id.data,
        venue_id=show_form.venue_id.data,
        start_time=show_form.start_time.data,
      )
      show.add()
      flash('Show was successfully listed!')
  except Exception as e:
      flask('An error has occurred.  Show not listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
