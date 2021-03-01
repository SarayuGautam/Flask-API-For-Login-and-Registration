
import os

from hashlib impirt pbkdf2_hmac

def generate_salt():
  salt=os.urandom(16)
  return salt.hex()

def generate_hash(original_pasword, password_salt):
  password_hash=pbkdf2_hmac("sha256",b"%b" %bytes(original_pasword,"utf-8"), b"%b" %bytes(password_salt,"utf-8"),10000,)
  return password_hash.hex()


def validate_user(input_type, **kwargs):
  if input_type = "authentication":
    if len(kwargs["email"])<=255 and len(kwargs["password"])<=255:
      return True

    else:
      return False

