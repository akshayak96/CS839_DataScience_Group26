import datetime
import os
import requests
import simplejson
import sqlite3
import urllib
 
from configobj import ConfigObj
 
#----------------------------------------------------------------------
def getMovieDetails(key, title):
    """
    Get additional movie details
    """
    if " " in title:
        parts = title.split(" ")
        title = "+".join(parts)
 
    link = "http://api.rottentomatoes.com/api/public/v1.0/movies.json"
    url = "%s?apikey=%s&q=%s&page_limit=1"
    url = url % (link, key, title)
    res = requests.get(url)
    js = simplejson.loads(res.content)
 
    for movie in js["movies"]:
        print "rated: %s" % movie["mpaa_rating"]
        print "movie synopsis: " + movie["synopsis"]
        print "critics_consensus: " + movie["critics_consensus"]
 
        print "Major cast:"
        for actor in movie["abridged_cast"]:
            print "%s as %s" % (actor["name"], actor["characters"][0])
 
        ratings = movie["ratings"]
        print "runtime: %s"  % movie["runtime"]
        print "critics score: %s" % ratings["critics_score"]
        print "audience score: %s" % ratings["audience_score"]
        print "for more information: %s" % movie["links"]["alternate"]
        saveData(movie)
    print "-" * 40
    print
 
#----------------------------------------------------------------------
def getInTheaterMovies():
    """
    Get a list of movies in theaters. 
    """
    today = datetime.datetime.today().strftime("%Y%m%d")
    config = ConfigObj("config.ini")
 
    if today != config["Settings"]["last_downloaded"]:
        config["Settings"]["last_downloaded"] = today
 
        try: 
            with open("config.ini", "w") as cfg:
                config.write(cfg)
        except IOError:
            print "Error writing file!"
            return
 
        key = config["Settings"]["api_key"]
        url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=%s"
        res = requests.get(url % key)
 
        data = res.content
 
        js = simplejson.loads(data)
 
        movies = js["movies"]
        for movie in movies:
            print movie["title"]
            getMovieDetails(key, movie["title"]) 
        print
 
#----------------------------------------------------------------------
def saveData(movie):
    """
    Save the data to a SQLite database
    """
    if not os.path.exists("movies.db"):
        # create the database
        conn = sqlite3.connect("movies.db")
 
        cursor = conn.cursor()
 
        cursor.execute("""CREATE TABLE movies 
        (title text, rated text, movie_synopsis text,
        critics_consensus text, runtime integer,
        critics_score integer, audience_score integer)""")
 
        cursor.execute("""
        CREATE TABLE cast
        (actor text, 
        character text)
        """)
 
        cursor.execute("""
        CREATE TABLE movie_cast
        (movie_id integer, 
        cast_id integer,
        FOREIGN KEY(movie_id) REFERENCES movie(id),
        FOREIGN KEY(cast_id) REFERENCES cast(id)
        )
        """)
    else:
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
 
    # insert the data
    print
    sql = "INSERT INTO movies VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (movie["title"],
                         movie["mpaa_rating"],
                         movie["synopsis"],
                         movie["critics_consensus"],
                         movie["runtime"],
                         movie["ratings"]["critics_score"],
                         movie["ratings"]["audience_score"]
                         )
                   )
    movie_id = cursor.lastrowid
 
    for actor in movie["abridged_cast"]:
        print "%s as %s" % (actor["name"], actor["characters"][0])
        sql = "INSERT INTO cast VALUES(?, ?)"
        cursor.execute(sql, (actor["name"],
                             actor["characters"][0]
                             )
                       )
        cast_id = cursor.lastrowid
 
        sql = "INSERT INTO movie_cast VALUES(?, ?)"
        cursor.execute(sql, (movie_id, cast_id) )
 
    conn.commit()
    conn.close()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    getInTheaterMovies()
