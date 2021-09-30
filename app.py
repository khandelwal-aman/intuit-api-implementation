from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from flask import Flask
from flask import request
from flask import redirect
import requests

app = Flask(__name__)


auth_client = AuthClient(
    'ABANF9dx522Cjhw5fi6j1eNEQZoGXxcb9R5eFADJiIOoqXsOfh',
    'h2YrzawWnkFDBAdCt4WBu5E6D3CcpLlwMThbSFh0',
    'http://localhost:5000/companyInfo',
    'sandbox',
)

scopes = [
    Scopes.ACCOUNTING,
]

auth_url = auth_client.get_authorization_url(scopes)

@app.route("/")
def main_page():
    
    if auth_client.access_token is None:
        return f'<a href="{auth_url}">{auth_url}</a>'
    else:
        return f'View Company Info'

@app.route("/companyInfo")
def company():
    d = request.args
    realm_id = d.get('realmId', None)
    auth_code = d.get('code', None)
    
    if realm_id is None or auth_code is None:
        return 'Error in auth code'
    else:
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
        
        base_url = 'https://sandbox-quickbooks.api.intuit.com'
        url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
        auth_header = 'Bearer {0}'.format(auth_client.access_token)
        headers = {'Authorization': auth_header, 'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        
        return response.text

