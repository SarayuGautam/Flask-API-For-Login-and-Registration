from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from dbConnect import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


app = Flask(__name__)

app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)


if __name__ == "__main__":
    app.run()

from auth_blueprint import authentication
app.register_blueprint(authentication, url_prefix="/api/auth")
