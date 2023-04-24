from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


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

    @app.route('/reset')
    def reset():
        # Drop all database 
        DB.drop_all()
        # Recreate all database tables according to the 
        # indcated schema in models.py
        DB.create_all()
        return render_template('base.html', title='Reset database')

    @app.route('/populate')
    def populate():
        # # create two fake users in DB
        add_or_update_user('elonmusk')
        add_or_update_user('rrherr')
        add_or_update_user('calebhicks')

        # ryan = User(id=1, username='Ryan')
        # DB.session.add(ryan)
        # vasan = User(id=2, username='Vasan')
        # DB.session.add(vasan)

        # # create two fake tweets in the DB
        # tweet1 = Tweet(id=1, text="ryan's tweet", user=ryan)
        # DB.session.add(tweet1)
        # tweet2 = Tweet(id=2, text="vasan's tweet", user=vasan)
        # DB.session.add(tweet2)

        # # Save the changes we just made to the database
        # # 'commit' the database changes
        # DB.session.commit()

        return render_template('base.html', title='Populate Database')

    @app.route('/update')
    def update():
        # get list of usernames of all users

        users = User.query.all()
        # usernames = []
        # for user in users:
        #     usernames.append(user.username)

        for username in [user.username for user in users]:
            add_or_update_user(username)

        return render_template('base.html', title='Users Updated')  

    return app
