import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
import json


# Obtain Bearer Token
def get_keycloak_token():
    keycloak_url = os.getenv('KEYCLOAK_TOKEN_URL')
    client_id = os.getenv('KEYCLOAK_CLIENT_ID')
    client_secret = os.getenv('KEYCLOAK_CLIENT_SECRET')
    realm = os.getenv('KEYCLOAK_REALM')

    # Keycloak token endpoint
    token_url = f'{keycloak_url}/realms/{realm}/protocol/openid-connect/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'  # For client credentials flow
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f'Failed to obtain token: {response.content}')

# encode query URL
def encode_url(metrics, arguments):
    params = {'query': metrics, **arguments}
    return urlencode(params)

# Make GET call
def get_metrics(encoded_url):
    base_url = os.getenv('BASE_URL')
    headers = {'Authorization': f'Bearer {get_keycloak_token()}'}
    response = requests.get(f'{base_url}{encoded_url}', headers=headers)
    return response.json()

# parse JSON response
def parse_json_response(data, parse_dict):
    parsed_data = {}
    if len(parse_dict['metric_list']) == 0:
        for entry in data['data']['result']:
            new_item = entry[parse_dict['entry']]
        parsed_data[parse_dict['entry']] = new_item
    else:
        for item in parse_dict['metric_list']:
            for entry in data['data']['result']:
                new_item = entry[parse_dict['entry']][item]
            parsed_data[item] = new_item
    return parsed_data


# Load environment variables from a .env file
load_dotenv('secrets.env')

# import inputs
input_dict = json.load(open('inputs.json'))

#Retrieve JSON parsing structure based on metric
parse_dict = json.load(open(input_dict['parse_profile'] + '.json'))

# main
# build query string + args & urlencode
metric_string = input_dict['metrics'] + '{' + 'acn_id="' + input_dict['acn'] + '", acc_id="' + input_dict['acc'] + '"}'
arguments = {'startDate': input_dict['time_start'], 'endDate': input_dict['time_end'], 'step': input_dict['step']}
encoded_url = encode_url(metric_string, arguments)

# send GET resquest to monitoring.powerflex.io
data = get_metrics(encoded_url)

# # Parse the JSON response
parsed_data = parse_json_response(data, parse_dict)

# # Print the parsed data
print(json.dumps(parsed_data, indent=4))
