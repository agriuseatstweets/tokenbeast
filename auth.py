from cryptography.fernet import Fernet
import tweepy
from gcsfs import GCSFileSystem
from environs import Env
from flask import Flask, request, Response, redirect, session
from os import path

env = Env()
CONSUMER_TOKEN = env('T_CONSUMER_TOKEN')
CONSUMER_SECRET = env('T_CONSUMER_SECRET')
CALLBACK_URL = env('BEAST_CALLBACK_URL')
TOKEN_LOCATION = env('TOKEN_LOCATION')
BEAST_SECRET = env('BEAST_SECRET')
GOOGLE_CLOUD_PROJECT = env('GOOGLE_CLOUD_PROJECT')

app = Flask(__name__)
app.secret_key = BEAST_SECRET

def write_out(key, secret):
    fs = GCSFileSystem(project=GOOGLE_CLOUD_PROJECT)
    crypt = Fernet(BEAST_SECRET)
    p = path.join(TOKEN_LOCATION, key)
    with fs.open(p, 'wb') as f:
        f.write(crypt.encrypt(f'{secret}'.encode('utf8')))

@app.route('/auth', methods=['GET'])
def handle_auth():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)


@app.route('/cb', methods=['GET'])
def handle_callback():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)
    auth.request_token = session.get('request_token')
    del session['request_token']
    verifier = request.args.get('oauth_verifier')
    try:
        key, secret = auth.get_access_token(verifier)
    except tweepy.TweepError as e:
        print('AUTH FAILED:')
        print(e)
        return e

    write_out(key, secret)
    return 'It worked. You\'ve added your token to the fight of of the Trollhunters. Thanks!'
