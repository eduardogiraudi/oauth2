from dotenv import load_dotenv
load_dotenv('.env') 
from flask import Flask
from flask import Flask, Response, request, url_for, redirect, make_response, render_template,jsonify
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import os
from flask_cors import CORS
import redis
from db import clients_collection, users_collection
import argon2
import cryptography #non rimuovere, fornisce il supporto a es512
from datetime import timedelta

app = Flask(__name__)
hasher = argon2.PasswordHasher(
    time_cost=4,
    memory_cost=131072,
    hash_len=64
) 
#scadenza dell'access token
expires = timedelta(minutes=15)
pepper=os.getenv('PEPPER')


@app.route('/logout', methods=['POST'])
@app.route('/authorize', methods=['POST'])
@app.route('/token', methods=['POST'])
@app.route('/login', methods=['POST'])
@app.route('/register', methods=['POST'])
@app.route('/change_password_with_otp', methods=['POST'])
def todo():
    pass