import os

class Config(object):
     SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-really-secret-key'
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
     SQLALCHEMY_TRACK_MODIFICATIONS = False
