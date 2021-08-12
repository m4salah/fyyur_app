import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

SQLALCHEMY_ECHO = True
# Connect to the database


# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = "postgresql://mohamed@localhost:5432/fyyurapp"
SQLALCHEMY_TRACK_MODIFICATIONS = False
