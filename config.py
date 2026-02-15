import os

# Get the absolute path of the project folder
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key'  # change to a random secret string
    # SQLite database inside instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
