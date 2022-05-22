import os
from flask import Flask, request, flash, redirect, url_for, g, render_template
from wprofile.db import get_db, get_people
from wprofile.people import People
from wprofile.person import Person

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wprofile.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET', 'POST'))
    def index():
        dbh = get_db()
        people = get_people(dbh)
        error = None
        if request.method == 'POST':
            print("Method = {}".format(request.method))
            name = request.form['username']
            phone_no = request.form['phone_no']
            email = request.form['email']
            if not name:
                error = 'Name is required'

            if error is None:
                pic = 0xffffffff
                try:
                    dbh.execute(
                        "INSERT INTO person (name, phone_no, email, picture)"
                        "VALUES (?, ?, ?, ?)", (name, phone_no, email, pic)
                    )
                    dbh.commit()
                    added_person = Person(name, phone_no, email, pic)
                    people.add(added_person)

                except db.IntegrityError:
                    error = f"User {name} is already added."
                else:
                    return redirect(url_for("index"))

            flash(error)
        # else: request.method == GET
        print("Length of g.people = {}".format(len(people)))
        return render_template("People.html", people=people.dict())
    from . import db
    db.init_app(app)
    return app