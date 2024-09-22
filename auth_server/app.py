from dotenv import load_dotenv
load_dotenv('.env') 
from flask import Flask
from flask import Flask, Response, request, url_for, redirect, make_response, render_template,jsonify
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import os
from flask_cors import CORS
import redis
from db import clients_collection, users_collection,jwt_banlist_collection
import argon2
import cryptography #non rimuovere, fornisce il supporto a es512
from datetime import timedelta

import responses

app = Flask(__name__)
CORS(app)


#setup per l'hasher argon2
hasher = argon2.PasswordHasher(
    time_cost=6,
    memory_cost=2**18,
    parallelism=4,
    hash_len=64,
    salt_len=16
)
pepper=os.getenv('PEPPER')



#setup jwt
app.config['JWT_ALGORITHM'] = 'ES512'
app.config['JWT_DECODE_ALGORITHMS'] = ['ES512']
app.config['JWT_PUBLIC_KEY'] = open('public_key.pem').read()
app.config['JWT_PRIVATE_KEY'] = open('private_key.pem').read()
jwt = JWTManager(app)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return responses.unauthorized(err="missing_token",descr="Missing token")
@jwt.invalid_token_loader
def invalid_token_response(callback):
    return responses.unauthorized(err="invalid_token", descr="Invalid token")
@jwt.expired_token_loader
def expired_token_response(callback ):
    return responses.unauthorized(err= "expired_token",descr="Expired token")
@jwt.revoked_token_loader
def revoked_token_response(callback):
    return responses.unauthorized(err="revoked_token",descr="Revoked token")
@jwt.needs_fresh_token_loader
def fresh_token_required_response(callback):
    return responses.unauthorized(err="refresh_token_required",descr="A fresh token is required")
@jwt.token_in_blocklist_loader
def check_if_token_is_in_blacklist(header,payload: dict):
    user_id = payload['sub']
    device = payload['device']
    user_banlist = jwt_banlist_collection.findOne({'user': ObjectId(user_id)})
    return True if user_banlist and device in user_banlist['banned_devices'] else False


#scadenza dell'access token
expires = timedelta(minutes=15)


@app.route('/logout', methods=['POST'])
@app.route('/authorize', methods=['POST'])
@app.route('/token', methods=['POST'])
@app.route('/login', methods=['POST'])
@app.route('/register', methods=['POST'])
@app.route('/change_password_with_recover_link', methods=['POST'])
@app.route('/change_password_with_token', methods=['POST'])
def todo():
    pass

@app.route('/refresh_token',methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    pass #determinare ancora la logica (vedere se utilizzare token a uso singolo etc, c'è anche da implementare il fingerprinting per la 2fa)