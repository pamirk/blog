import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MY-VERY-PRIVATE-AND-SECRETE-KEY-THAT-NO-ONE-CAN-GUESS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Mail_SERVER = os.environ.get('MAIL_SERVER')
    Mail_PORT = int(os.environ.get('MAIL_PORT') or 25)
    Mail_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    Mail_USERNAME = os.environ.get('MAIL_USERNAME')
    Mail_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['pamirkhan11@gmail.com']