from flask import Flask
from flaskext.mysql import MySQL
app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL()
# app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pictures'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
from app import views