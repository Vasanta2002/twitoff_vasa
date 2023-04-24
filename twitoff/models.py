from flask_sqlalchemy import SQLAlchemy

# create database object from SQLAlchemy class

DB = SQLAlchemy()


class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column.
    username = DB.Column(DB.String, nullable=False)
    # most rescent tweet id
    newest_tweet_id = DB.Column(DB.BigInteger)
    # backref is as-if we had added a tweets list to the user class
    # tweets = []
    # so user to find tweet, or tweet to find user

    def __reper__(self):
        return f"User: {self.username}"


class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column
    text = DB.Column(DB.Unicode(300))
    # store our word embeddings "vectorization"
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id column (foreign / secondary key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # user column creates a two-way link between a user object and a tweet
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __reper__(self):
        return f"Tweet: {self.text}"
