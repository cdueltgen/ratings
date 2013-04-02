import model
import csv
import datetime
from time import strptime

def load_users(session):
    # use u.user
    # data looks like 1|24|M|technician|85711
    with open('seed_data/u.user', 'rb') as input_file:
        read_input = csv.reader(input_file, delimiter='|')
        for row in read_input:
            user = model.User(id=row[0], email="email", password="password", age = row[1], zipcode = row[4])
            session.add(user)
        session.commit()


def load_movies(session):
    # use u.item
    # input looks like 1|Toy Story (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0
    # Line 267 has invalid/empty date
    with open('seed_data/u.item', 'rb') as input_file:
        read_input = csv.reader(input_file, delimiter='|')
        for row in read_input:
            # This code exists for parsing the release date. It fails on an empty date
            if row[2] == "":
                release_date = datetime.datetime.strptime("01-Jan-1900", "%d-%b-%Y")
            else:
                release_date = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            # These are all things I tried before I figured out the stuff above
            # Keeping for posterity
            #split_date = row[2].split('-')
            #month_num = strptime(split_date[1], '%b').tm_mon
            #month_num = list(calendar.month_abbr).index(split_date[1])
            #format_date = datetime.date(split_date[2], split_date[1], split_date[0])
            #print row[0], split_date

            # Convert the movie title to unicode
            title = row[1]
            title = title.decode("latin-1")
            # Here's where the actual code for populating the movies goes.
            movie = model.Movie(id = row[0], name=title, released_at=release_date, imdb_url=row[4])
            session.add(movie)
        session.commit()


def load_ratings(session):
    # use u.data
    # input looks like 196  242 3   881250949
    with open('seed_data/u.data', 'rb') as input_file:
        read_input = csv.reader(input_file, delimiter="\t")
        for row in read_input:
            data = model.Rating(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(data)
        session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
