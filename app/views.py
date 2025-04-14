"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf
import traceback
import os


###
# Routing for your application.
###

UPLOAD_FOLDER = 'uploads'  # Or your desired folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create if it doesn't exist

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    """
    Handles POST requests to add a new movie.
    Validates form data, saves the poster, and stores movie details in the database.
    Returns a JSON response with either success or validation error messages.
    """

    form = MovieForm(request.form)

    print("----- Flask - Full Request -----")
    print("request:", request)
    print("----- Flask request.form -----")
    print(request.form)
    print("----- Flask request.files -----")
    print(request.files)

    if form.validate_on_submit():
        print("----- Flask - form.validate_on_submit() - Passed -----")
        print("----- Flask form.data -----")
        print("form.data:", form.data)

        try:
            # 1. Handle File Upload
            poster_file = form.poster.data  # Access file from form
            filename = secure_filename(poster_file.filename)
            poster_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            poster_file.save(poster_path)

            # 2. Create Movie Object
            movie = Movie(
                title=form.title.data,
                description=form.description.data,
                poster=filename  # Store only the filename
            )

            # 3. Save to Database
            db.session.add(movie)
            db.session.commit()

            # 4. Return Success Response
            return jsonify({
                "message": "Movie Successfully added",
                "title": movie.title,
                "poster": movie.poster,
                "description": movie.description
            }), 201  # 201 Created status code

        except Exception as e:
            print("----- Flask - Exception -----")
            traceback.print_exc()
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500

    else:
        print("----- Flask - form.validate_on_submit() - Failed -----")
        print("----- Flask form.errors -----")
        print("form.errors:", form.errors)
        print("----- Flask form_errors() Output -----")
        print("form_errors(form):", form_errors(form))
        return jsonify({"errors": form_errors(form)}), 400


@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_data = {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": f"/api/v1/posters/{movie.poster}"  # Construct the poster URL
        }
        movie_list.append(movie_data)
    return jsonify({"movies": movie_list})

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(upload_path)

def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        try:
            field_label = getattr(form, field).label.text
        except AttributeError:
            field_label = field  # Or some default value
        for error in errors:
            message = f"Error in {field_label}: {error}"
            error_messages.append(message)
    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404