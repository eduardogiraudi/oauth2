from dotenv import load_dotenv
load_dotenv('.env') 
from flask import Flask, Response,session, request, url_for, redirect, make_response, render_template,jsonify
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import os
from flask_cors import CORS
import redis
from db import clients_collection, users_collection,jwt_banlist_collection
import argon2
import cryptography #non rimuovere, fornisce il supporto a es512
from datetime import datetime, timedelta
from decorators import require_args, require_params
from urllib.parse import urlparse
from utils import verify_code_verifier
from db import redis_client
import responses
from json import loads,dumps

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



#setup jwt
app.config['JWT_ALGORITHM'] = 'ES512'
app.config['JWT_DECODE_ALGORITHMS'] = ['ES512']
app.config['JWT_PUBLIC_KEY'] = open('public.pem').read()
app.config['JWT_PRIVATE_KEY'] = open('private.pem').read()
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
    user_banlist = jwt_banlist_collection.find_one({'user': ObjectId(user_id)})
    return True if user_banlist and device in user_banlist['banned_devices'] else False


#scadenza dell'access token
expires = timedelta(minutes=5)
supported_grant_types = ['authorization_code']
pepper=os.getenv('PEPPER')


@require_params(['grant_type', 'code', 'redirect_uri', 'client_id','code_verifier'])
@app.route('/token', methods=['POST'])
def token():
    data = request.get_json()
    grant_type = data.get('grant_type')
    authorization_code = data.get('code')
    saved_info = redis_client.get(loads(authorization_code))
    code_challenge = saved_info['code_challenge']
    saved_authorization_code = saved_info['authorization_code']
    redirect_uri = data.get('redirect_uri')
    client_id = data.get('client_id')
    code_verifier = data.get('code_verifier')

    '''VERIFICA CHE IL GRANT TYPE SIA SUPPORTATO'''
    if grant_type not in supported_grant_types:
        return responses.bad_request(err='unsupported_grant_type',descr='Unsupported grant type')
    '''
    FINE VERIFICA  GRANT TYPE
    '''
    '''
    VERIFICA CHE NON SIA SCADUTO
    '''
    if datetime.utcnow() > saved_info['expiration_date']:
        return responses.bad_request(err='invalid_grant',descr='Authorization code expired')
    '''
    FINE VERIFICA CHE NON SIA SCADUTO
    '''
    '''
    VERIFICA DEL CLIENT
    '''
    #controllo se il client è registrato e il redirect uri è associato al client
    client = clients_collection.find_one({'client_id': client_id})
    if not client:
        return responses.bad_request(err='invalid_client',descr='Client not found')
    parsed_redirect_uri = urlparse(redirect_uri)
    client_redirect_uri = urlparse(client['redirect_uri'])
    if parsed_redirect_uri.netloc != client_redirect_uri.netloc:
        return responses.bad_request(err='invalid_client',descr='Redirect uri does not match with the client')
    '''
    FINE VERIFICA DEL CLIENT
    '''
    '''
    VERIFICA DEL CODE VERIFIER
    '''
    if not verify_code_verifier(code_verifier, code_challenge):
        return responses.bad_request(err='invalid_grant',descr='Invalid code verifier')
    '''
    FINE VERIFICA DEL CODE VERIFIER
    '''
    '''
    VERIFICA DEL CODE
    '''
    if not saved_authorization_code or saved_authorization_code != authorization_code:
        return responses.bad_request(err='invalid_grant',descr='Invalid authorization code')
    '''
    FINE VERIFICA DEL CODE
    '''

    '''
    INVALIDA IL CODE
    '''
    redis_client.delete(loads(authorization_code))
    '''
    FINE INVALIDA IL CODE
    '''
    '''
    GENERAZIONE DEL TOKEN
    '''

    '''TODO guardare come gestire e generare i token'''
    id_token_payload = {
        # 'sub': 'user_id',  
        'aud': client_id,
        'exp': datetime.utcnow() + expires,
        'iat': datetime.utcnow(),
        'iss': 'auth_server',
        'sub': 'user_id',#il sub va recuperato dal server di risorse tramite una chiamata redis
        # 'nonce': data.get('nonce')  # Se usi nonce, includilo
    }
    token=create_access_token(identity='user_id', expires_delta=expires)
    refresh_token=create_refresh_token(identity='user_id', expires_delta=expires)
    id_token = jwt.encode(id_token_payload, app.config['JWT_PRIVATE_KEY'], algorithm='ES512')
    return responses.ok(data={
        'access_token': token, 
        'refresh_token': refresh_token, 
        'id_token': id_token,
        'token_type': 'Bearer',
        'expires_in': expires.total_seconds()
        })







@app.route('/revoke', methods=['POST'])
def revoke():
    pass 

@app.route('/introspect', methods=['POST'])
def introspect():
    pass


@app.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, expires_delta=expires)
    id_token_payload = {
        'aud': 'client_id',  
        'exp': datetime.utcnow() + expires,
        'iat': datetime.utcnow(),
        'iss': 'auth_server',
        'sub': current_user,
    }
    id_token = jwt.encode(id_token_payload, app.config['JWT_PRIVATE_KEY'], algorithm='ES512')
    return responses.ok(data={
        'access_token': new_access_token,
        'id_token': id_token,  
        'token_type': 'Bearer',
        'expires_in': expires.total_seconds()
    })

'''ROTTE CUSTOM INTERNE'''
@require_params(['username', 'password'])
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = users_collection.find_one({'$or': [{'username': username}, {'email': username}]})
    if user:
        return responses.bad_request(err='user_already_exists',descr='User already exists')
    user = {
        'username': username,
        'password': hasher.hash(password+pepper),
        #'email': ????
    }
    users_collection.insert_one(user)
    pass
@app.route('/logout', methods=['POST'])
@app.route('/change_password_with_recover_link', methods=['POST'])
@app.route('/change_password_with_token', methods=['POST'])
@app.route('/forgot_password', methods=['POST'])
def pass_():
    pass
@require_params(['username', 'password'])
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = users_collection.find_one({'$or': [{'username': username}, {'email': username}]})
    if not user:
        return responses.not_found(err='user_not_found',descr='User not found')
    try:   
        needs_rehash = hasher.check_needs_rehash(user["password"]) 
        hasher.verify(hash=user["password"],password=password+pepper) 
        if needs_rehash:
            user["password"] = hasher.hash(password+pepper)
            users_collection.update_one({'_id': user['_id']}, {'$set': {'password': user["password"]}})
        pass 
        #vedere che fare mo, soprattutto come, sicuramente è necessaria la memorizzazione di sessione, ma bisogna
        #fare attenzione a evitare che diverse sessioni legate allo stesso utente collidano
        #sicureamente è usabile lo scope, il client_id, il redirect_uri, il code_challenge
    except argon2.exceptions.VerifyMismatchError:
        return responses.bad_request(err='invalid_credentials',descr='Invalid credentials')



@require_params(['response_type', 'client_id', 'redirect_uri', 'scope', 'state'])
@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        client_id = request.args.get('client_id')
        redirect_uri = request.args.get('redirect_uri')
        response_type = request.args.get('response_type')
        scope = request.args.get('scope')  # Scope richiesto dal client
        state = request.args.get('state')
        client = clients_collection.find_one({'client_id': client_id})
        if not client or redirect_uri != client['redirect_uri']:
            return responses.bad_request(err='invalid_client', descr='Invalid client or redirect URI')
        return render_template('authorize.html', client=client, scope=scope, state=state)

    elif request.method == 'POST':
        # Gestisci la conferma dell'utente
        user_id = request.form.get('user_id')  # Supponendo che l'utente sia autenticato
        client_id = request.form.get('client_id')
        redirect_uri = request.form.get('redirect_uri')
        scope = request.form.get('scope')  # Scope approvato dall'utente
        state = request.form.get('state')

        # Genera un authorization code
        authorization_code = generate_authorization_code()
        redis_client.set(authorization_code, dumps({
            'user_id': user_id,
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,  # Salva lo scope approvato
            'expiration_date': datetime.utcnow() + timedelta(minutes=10)
        }))
        # Reindirizza al redirect_uri con il codice di autorizzazione
        return redirect(f"{redirect_uri}?code={authorization_code}&state={state}")


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
@app.route('/register', methods=['GET'])
@app.route('/forgot_password', methods=['GET'])
@app.route('/change_password_with_recover_link', methods=['GET'])
def index():
    return render_template('index.html')
