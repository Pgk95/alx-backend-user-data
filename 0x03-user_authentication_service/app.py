#!/usr/bin/env python3
"""flask app"""
from flask import Flask, render_template, request, jsonify, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """index"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register"""
    if request.form.get('email') and request.form.get('password'):
        try:
            user = AUTH.register_user(request.form.get('email'),
                                      request.form.get('password'))
            return jsonify({"email": user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login"""
    if request.form.get('email') and request.form.get('password'):
        if AUTH.valid_login(request.form.get('email'),
                            request.form.get('password')):
            session_id = AUTH.create_session(request.form.get('email'))
            response = jsonify({"email": request.form.get('email'),
                                "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
        else:
            abort(401)
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """profile"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """reset password"""
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": reset_token})
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def new_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify({"email": email, "message": "Password updated"})
        except ValueError:
            abort(403)
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
