"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Ratings
from model import Movies
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    print("Movies")

    for row in open("seed_data/u.item"):
        row = row.strip()
        movie_id, title, released_at, blank, imdb_url, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen = row.split("|")
        
        delete_year = slice(0, len(title)-7)
        title = title[delete_year]

        if released_at:
            released_at = datetime.strptime(released_at, "%d-%b-%Y")

        movies = Movies(movie_id=movie_id,
                        title=title,
                        released_at=released_at,
                        imdb_url=imdb_url)
        
        db.session.add(movies)
        db.session.commit()        


def load_ratings():
    """Load ratings from u.data into database."""
    print("Ratings")
    id = 0
    for row in open('seed_data/u.data'):
        id += 1
        row = row.strip().split("\t")
        
        rating_id = id
        user_id = row[0]
        movie_id = row[1]
        score = row[2]

        rating = Ratings(rating_id=rating_id,
                         user_id=user_id,
                         movie_id=movie_id,
                         score=score)

        db.session.add(rating)
        db.session.commit()
        


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    # load_movies()
    load_ratings()
    set_val_user_id()
