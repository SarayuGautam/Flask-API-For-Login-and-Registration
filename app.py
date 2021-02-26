from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MYSQL
from dbConnect import MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD

app=FLASK(__name__)

app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"]= MYSQL_PASSWORD
app.config["MYSQL_DB"]= MYSQL_DB
app.config["MYSQL_CURSORCLASS"]= "DictCursor"

db = MYSQL(app)
