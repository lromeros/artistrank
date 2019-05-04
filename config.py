import os

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        (key, value) = line.strip().split('=')
        os.environ[key] = value


def spotify_client_id():
    return os.environ.get('SPOTIFY_CLIENT_ID')


def spotify_client_secret():
    return os.environ.get('SPOTIFY_CLIENT_SECRET')
