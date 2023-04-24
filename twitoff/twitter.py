from os import getenv
import not_tweepy as tweepy
from .models import DB, Tweet, User
import spacy

# get our api keys from .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# connect to the twitter api
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    '''take a username and pull that user's data and tweets from the API
    if this user already exists in our database then we will just check to
    see if there are any new tweets from the user that we don't already have
    and we will add any new tweets to the DB.'''
    try:
        # get the user information from twitter
        twitter_user = TWITTER.get_user(screen_name=username)

        # check to see if user is already in the database
        # If we dont already have that user, then we'll create a new one
        db_user = (User.query.get(twitter_user.id)) or (User(id=twitter_user.id, username=username))

        # add the user to the database
        # this wont re-add the user if they are already been added
        DB.session.add(db_user)

        # get the users wteets (in a list)
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)
        
        # update the newest_tweet_id if there have been new tweets
        # since the last time this user tweeted
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add all the individual tweets to the database

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector,
                             user_id=db_user.id)

            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        # save the changes to the DB
        DB.session.commit()


nlp = spacy.load('my_model/')
# give function some text, it returns a word embedding

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
