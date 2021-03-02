from flask import Blueprint, request, Response, jsonify
from utils import (
    validate_user_input,
    generate_salt,
    generate_hash,
    db_write,
    validate_user,
)

authentication = Blueprint("authentication",__name__)

@authentication.route("/register",methods=["POST"])
def register():
  email=request.json["email"]
  password=request.json["password"]
  confirm_password = request.json["confirm_password"]

  if password==confirm_password and validate_user("authentcation",email,password):
    password_salt=generate_salt()
    password_hash=generate_hash(password,password_salt)

    if db_write("""INSERT INTO users (email,password_salt,password_hash) VALUES (%s,%s,%s)""",(email,password_salt,password_hash),):
      return Response(status=201)
    else:
      return Response(status=409)
  else:
    return Response(status=400)


@authentication.route("/login",methods=["POST"])
def login():
  email=request.json["email"]
  password=request.json["password"]

  user_token = validate_user(email,password)

  if user_token:
    return jsonify({"jwt_token":user_token})
  else:
    Response(status=401)
