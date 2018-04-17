"""
GET /profiles
Description:
Get a list of all profiles formatted in an html file
Parameters:
None

GET /profiles/api
Description:
Get a list of all profiles in json format
Parameters:
None

GET /locations
Description:
Get a list of all locations formatted in an html file
Parameters:
None

GET /locations/api
Description:
Get a list of all locations in json format
Parameters:
None

GET /favorites
Description:
Get a list of all favorites formatted in an html file
Parameters:
None

GET /favorites/api
Description:
Get a list of all favorites in json format
Parameters:
None

POST /
Description:
Add items to profiles, locations, and favorites table
Parameters:
request forms

GET /
Description:
Get html template containing forms for the POST method
Parameters:
None
"""

from flask import Flask, g, jsonify, request, render_template
import os
import sqlite3


app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'project_sql.sqlite')


def init_db():
    """
    Create database file with schema
    :return: None
    """
    conn = get_db()

    project_sql = '''
    DROP TABLE IF EXISTS Profiles;
    DROP TABLE IF EXISTS Locations;
    DROP TABLE IF EXISTS Favorites;
    CREATE TABLE Profiles (
        Profile_id INTEGER PRIMARY KEY,
        First_name TEXT,
        Last_name TEXT
    );
    CREATE TABLE Locations (
        Location_id INTEGER PRIMARY KEY,
        City TEXT,
        Country TEXT,
        Profile_id INTEGER NOT NULL,
        FOREIGN KEY ([Profile_id]) REFERENCES [Profile] ([Profile_id])
    );
    CREATE TABLE Favorites(
        Favorites_id INTEGER PRIMARY KEY,
        Soda TEXT,
        Candy TEXT,
        Profile_id INTEGER NOT NULL,
        FOREIGN KEY ([Profile_id]) REFERENCES [Profile] ([Profile_id]));'''

    conn.cursor().executescript(project_sql)


@app.cli.command('initdb')
def initdb_command():
    """
    Create database file via commandline
    :return: None
    """
    init_db()
    print('Initialized the database.')


def connect_db():
    """
    Returns a sqlite connection object associated with the application's
    database file.
    """
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row

    return conn


def get_db():
    """
    Returns a database connection. If a connection has already been created,
    the existing connection is used, otherwise it creates a new connection.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


def query_by_id(table_name, item_id):
    """
    Get a row from a table that has a primary key attribute named id.

    Returns None of there is no such row.

    :param table_name: name of the table to query
    :param item_id: id of the row
    :return: a dictionary representing the row
    """
    conn = get_db()
    cur = conn.cursor()

    id_var = table_name + '_id'

    query = 'SELECT * FROM {} WHERE {} = ?'.format(table_name, id_var)

    cur.execute(query, (item_id,))

    row = cur.fetchone()

    if row is not None:
        return dict(row)
    else:
        return None


def insert_data(first_name, last_name, city, country, soda, candy):
    """
    Insert all data into database tables
    :param first_name: First name of the user
    :param last_name: Last name of the user
    :param city: City where user came from
    :param country: Country where user came from
    :param soda: User's favorite soda
    :param candy: User's favorite candy
    :return:
    """
    conn = get_db()

    cur = conn.cursor()

    query = 'INSERT INTO Profiles(First_name, Last_name) VALUES(?, ?)'
    cur.execute(query, (first_name, last_name))
    item_id = cur.lastrowid

    query = 'INSERT INTO Locations(City, Country, Profile_id) VALUES(?, ?, ?)'
    cur.execute(query, (city, country, item_id))

    query = 'INSERT INTO Favorites(Soda, Candy, Profile_id) VALUES(?, ?, ?)'
    cur.execute(query, (soda, candy, item_id))

    conn.commit()


def get_all_rows(table_name):
    """
    Returns all of the rows from a table as a list of dictionaries. This is
    suitable for passing to jsonify().

    :param table_name: name of the table
    :return: list of dictionaries representing the table's rows
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'SELECT * FROM {}'.format(table_name)

    results = []

    for row in cur.execute(query):
        results.append(dict(row))

    return results


@app.route('/profiles/api')
def profile_api():
    """
    Implements GET /profiles in json format

    :return: JSON response containing all profiles
    """
    profiles = get_all_rows('Profiles')

    # Flask's jsonify() function creates a flask.Response object containing
    # a JSON representation of the provided object with a status code of 200.
    return jsonify(profiles)


@app.route('/profiles')
def get_profiles():
    """
    Returns a list containing all the profiles in the database.
    :return: render profiles.html template
    """
    conn = get_db()
    cur = conn.cursor()

    profiles = []

    for row in cur.execute('SELECT Last_name, First_name FROM Profiles'):
        profiles.append((row['Last_name'], row['First_name']))

    return render_template('profiles.html', profiles=profiles)


@app.route('/locations/api')
def locations_api():
    """
    Implements GET /location in json format

    :return: JSON response containing all location items
    """

    locations = get_all_rows('Locations')

    # Flask's jsonify() function creates a flask.Response object containing
    # a JSON representation of the provided object with a status code of 200.
    return jsonify(locations)


@app.route('/locations')
def get_locations():
    """
    Returns a list containing all the locations in the database.
    :return: render locations.html template
    """
    conn = get_db()
    cur = conn.cursor()

    locations = []

    for row in cur.execute('SELECT City, Country FROM Locations'):
        locations.append((row['City'], row['Country']))

    return render_template('locations.html', locations=locations)


@app.route('/favorites/api')
def favorites_api():
    """
    Implements GET /favorites in json format

    :return: JSON response containing all favorite items
    """

    favorites = get_all_rows('Favorites')

    # Flask's jsonify() function creates a flask.Response object containing
    # a JSON representation of the provided object with a status code of 200.
    return jsonify(favorites)


@app.route('/favorites')
def get_favorites():
    """
    Returns a list containing all the favorites in the database.
    :return: render favorites.html template
    """
    conn = get_db()
    cur = conn.cursor()

    favorites = []

    for row in cur.execute('SELECT Candy, Soda FROM Favorites'):
        favorites.append((row['Candy'], row['Soda']))

    return render_template('favorites.html', favorites=favorites)


@app.route("/", methods=['GET', 'POST'])
def start_up():
    """
    Main domain function for that has web forms for users to post
    :return: render add_to_db.html template containing
    """
    if request.method == 'POST':
        first_name = request.form['First_name']
        last_name = request.form['Last_name']
        city = request.form['City']
        country = request.form['Country']
        soda = request.form['Soda']
        candy = request.form['Candy']

        insert_data(first_name, last_name, city, country, soda, candy)
        return render_template('add_to_db.html', First_name=first_name,
                               Last_name=last_name, City=city,
                               Country=country, Soda=soda, Candy=candy)
    elif request.method == 'GET':
        return render_template('add_to_db.html')
