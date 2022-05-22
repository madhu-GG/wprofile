import sqlite3, click
from sqlite3 import IntegrityError
from flask import g, current_app
from flask.cli import with_appcontext
from wprofile.people import People
from wprofile.person import Person

def get_people(dbh):
    if 'people' not in g:
        g.people = People()
        try:
            res = dbh.execute('SELECT * FROM person')
        except:
            return g.people
        else:
            for name, phone_no, email, pic in res:
                person = Person(name, phone_no, email, pic)
                g.people.add(person)
        
    return g.people

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    people = get_people()
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    if len(people) > 0:
        del(people)
        del(g.people)
        g.people = People()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ clear the existing data and create new tables """
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)