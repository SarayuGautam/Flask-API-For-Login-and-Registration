from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL, MySQLdb
from dbConnect import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, JWT_SECRET_KEY
from hashlib import pbkdf2_hmac


import os
import jwt

app = Flask(__name__)

app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)

def generate_salt():
  salt=os.urandom(16)
  return salt.hex()

def generate_hash(original_pasword, password_salt):
  password_hash=pbkdf2_hmac("sha256",b"%b" %bytes(original_pasword,"utf-8"), b"%b" %bytes(password_salt,"utf-8"),10000,)
  return password_hash.hex()


def validate_user_input(input_type, **kwargs):
  if input_type == "authentication":
    if len(kwargs["email"])<=255 and len(kwargs["password"])<=255:
      return True

    else:
      return False

def db_write(query,params):
  cursor = db.connection.cursor()
  try:
    cursor.execute(query,params)
    db.connection.commit()
    cursor.close()

    return True
  except MySQLdB._exceptions.IntegrityError:
    cursor.close()
    return False

def db_read(query,params=None):
  cursor=db.connection.cursor()
  if params:
    cursor.execute(query,params)
  else:
    cursor.execute(query)
  entries = cursor.fetchall()
  cursor.close()
  content=[]
  for entry in entries:
    content.append(entry)
  return content

def generate_jwt_token(content):

  return jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")

def validate_user(email,password):
  current_user=db_read("""SELECT * FROM users WHERE email = %s""",(email,))

  if len(current_user)==1:

    saved_password_hash=current_user[0]["password_hash"]
    saved_password_salt=current_user[0]["password_salt"]

    password_hash=generate_hash(password,saved_password_salt)

    if password_hash==saved_password_hash:
      user_id=current_user[0]["id"]
      return generate_jwt_token({"id":user_id})
    else:
      return False
  else:
    return False

@app.route("/register", methods=["GET","POST"])
def register_user():
  user_email = request.json["email"]
  user_password = request.json["password"]
  user_confirm_password = request.json["confirm_password"]

  if user_password == user_confirm_password and validate_user_input(
      "authentication", email=user_email, password=user_password
  ):
      password_salt = generate_salt()
      password_hash = generate_hash(user_password, password_salt)

      if db_write(
          """INSERT INTO users (email, password_salt, password_hash) VALUES (%s, %s, %s)""",
          (user_email, password_salt, password_hash),
      ):
          return Response(status=201)
      else:
          return Response(status=409)
  else:
      return Response(status=400)


@app.route("/login", methods=["GET","POST"])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user(user_email, user_password)
    if user_token:
        return jsonify({"token": user_token})
    else:
        return Response(status=401)

if __name__ == "__main__":
    app.run(debug=True)


