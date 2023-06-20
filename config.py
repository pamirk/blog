import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MY-VERY-PRIVATE-AND-SECRETE-KEY-THAT-NO-ONE-CAN-GUESS'
