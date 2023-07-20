# database setting
# mysql
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'web_cwk2'
# USERNAME = 'root'
# PASSWORD = 'Cpczhendeshuai4'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI

# sqlite
from os import path

basedir = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + path.join(basedir, 'database.sqlite')

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

SECRET_KEY = "jjjjjj"

# flask-mail setting
# using qq_mail in the project
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True  # if published, change to False
MAIL_USERNAME = "1228665611@qq.com"
MAIL_PASSWORD = "arwthviobpougfjb"
MAIL_DEFAULT_SENDER = "1228665611@qq.com"
