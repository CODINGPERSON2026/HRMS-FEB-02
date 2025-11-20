from flask import Flask,redirect,request
import jwt
JWT_SECRET = "MY_SUPER_SECRET_KEY_123"      # change this later
JWT_ALGO = "HS256"
def require_login():
    token = request.cookies.get("token")
    if not token:
        return None  # Not logged in

    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return data
    except Exception:
        return None
