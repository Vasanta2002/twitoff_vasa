from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():

    app = Flask(__name__)

    # database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # register out database with the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/bananas')
    def bananas():
        return render_template('base.html', title='Bananas')

    @app.route('/reset')
    def reset():
        # Drop all database 
        DB.drop_all()
        # Recreate all database tables according to the 
        # indcated schema in models.py
        DB.create_all()
        return "database had been reset"

    @app.route('/populate')
    def populate():
        # create two fake users in DB
        ryan = User(id=1, username='Ryan')
        DB.session.add(ryan)
        vasan = User(id=2, username='Vasan')
        DB.session.add(vasan)

        # create two fake tweets in the DB
        tweet1 = Tweet(id=1, text="ryan's tweet", user=ryan)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="vasan's tweet", user=vasan)
        DB.session.add(tweet2)

        # Save the changes we just made to the database
        # 'commit' the database changes
        DB.session.commit()

        return "database has been populated"

    return app
