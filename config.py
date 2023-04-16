import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Random string (key) used to secure the sessions that remember info from one request to another
    SECRET_KEY = os.urandom(24)  # generate a string of random characters of size 24

    # Configuring Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"  # Google SMTP server address
    MAIL_PORT = 465  # Gmail SMTP port (TLS)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "ownmyhome.csc450@gmail.com"
    # MAIL_PASSWORD = "csc450SoftwareEngineering!"
    MAIL_PASSWORD = "lbuhsobvyoodshlh"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

