#encoding: utf-8

import os

DEBUG=True

SECRET_KEY = os.urandom(24)

DIALET = 'mysql'
DRIVER = 'pymysql'
HOST   = '127.0.0.1'
PORT   = 3306
USERNAME = 'root'
PASSWORD = 'cyl17600109104'
DATABASE = 'company'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALET,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

