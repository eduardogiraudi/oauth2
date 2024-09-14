from dotenv import load_dotenv
import json
import os
import uuid
load_dotenv('/.env')

authorized_redirect_domain = os.getenv('AUTHORIZED_REDIRECT_DOMAIN')
client_data = {
    "client_id": str(uuid.uuid4()),
    "authorized_redirects": authorized_redirect_domain.split(',')
}
with open('client.json', 'w') as json_file:
    json.dump(client_data, json_file, indent=4)