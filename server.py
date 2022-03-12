"""Movie Ratings."""

from collections import UserList
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Ratings, Movies


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def show_register():
    return render_template("register.html")

@app.route('/register', methods=["POST"])
def process_register():
    user_email = request.form['email']
    user_passwod = request.form['password']
    user_age = request.form['age']
    user_zipcode = request.form['zipcode']

    users = User.query.all()
    
    for user in users:
        if user.email == user_email:
            flash("Email Already Exists")
            return redirect(url_for('show_register'))

    new_user = User(email=user_email, password=user_passwod, age=user_age, zipcode=user_zipcode)
    db.session.add(new_user)
    db.session.commit()
    flash("You have been registered!")
    return redirect(url_for('index'))

@app.route('/login', methods=["GET"])
def show_login():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def process_login():
    user_email = request.form['email']
    user_password = request.form['password']

    users_list = User.query.all()
    for user in users_list:
        if user.email == user_email and user.password == user_password:
            flash("You are logged in!")
            session['email'] = user_email
            return redirect(url_for('index', user=user))
        elif user.email == user_email and not user.password == user_password:
            flash("Incorrect Password")
            return redirect(url_for('show_login'))
            
    flash("Email not found")
    return redirect(url_for('show_login'))


@app.route('/users/<user_id>')
def user_page(user_id):
    user = User.query.get(user_id)
    ratings = Ratings.query.filter_by(user_id=user_id).all()
    movies = []
    movie_dict = {}
    for rating in ratings:
        movie_id = rating.movie_id
        movie = Movies.query.get(movie_id)
        movies.append(movie.title)
    
    i = 0
    for movie in movies:
        movie_dict[movie] = ratings[i]
        i+=1
    
    print(movie_dict)
    return render_template('user_info.html', user=user, movies=movie_dict)
    


@app.route('/logout')
def logout():
    session['email'] = ""
    flash("You have been logged out!")
    return redirect(url_for('index'))











if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
