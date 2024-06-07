import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
import json


# Obtain Bearer Token
def get_netcloud_auth():
    x_cp_api_id = os.getenv('X-CP-API-ID')
    x_cp_api_key = os.getenv('X-CP-API-KEY')
    x_ecm_api_id = os.getenv('X-ECM-API-ID')
    x_ecm_api_key = os.getenv('X-ECM-API-KEY')

    return {"X-CP-API-ID": x_cp_api_id, "X-CP-API-KEY": x_cp_api_key, "X-ECM-API-ID": x_ecm_api_id, "X-ECM-API-KEY": x_ecm_api_key,}

# encode query URL
def encode_url(metrics, arguments):
    params = {'query': metrics, **arguments}
    return urlencode(params)

# Make GET call
def get_metrics(metrics):
    base_url = os.getenv('BASE_URL_NC')
    headers = get_netcloud_auth()
    response = requests.get(f'{base_url}{metrics}', headers=headers)
    return response.json()

# parse JSON response
def parse_json_response_nc(data, parse_dict):
    parsed_data = []
    for entry in data[parse_dict['entry']]:
        parsed_event = {}
        for item in parse_dict['metric_list']:
            new_item = entry[item]
            parsed_event[item] = new_item
        parsed_data.append(parsed_event)
    return parsed_data

# Make list of router urls
def pull_router_url(alert_dict):
    router_urls = []
    for item in alert_dict:
        router = item['router']
        router_urls.append(router)
    return router_urls

# pull out acn-acc from description
def acn_acc_extract(router_details):
    for router in router_details:
        separate_out_acn = router['description'].split('-')
        if len(separate_out_acn) > 2:
            separate_out_acc = separate_out_acn[2].split(' ')
            router['acn'] = separate_out_acn[1]
            router['acc'] = separate_out_acc[0]
    return router_details

# extract additional details from individual routers
def grab_router_details(router_urls, parse_dict):
    headers = get_netcloud_auth()
    router_details = []
    for site in router_urls:
        router_full_details = requests.get(site, headers=headers).json()
        parsed_event = {}
        for item in parse_dict['router_list']:
            parsed_event[item] = router_full_details[item]
        router_details.append(parsed_event)
    router_details = acn_acc_extract(router_details)
    return router_details

# router-specific details added to alert details
def combine_alert_with_router(parsed_data, router_details):
    for alert, router in zip(parsed_data, router_details):
        for item in router.keys():
            alert[item] = router[item]
    return parsed_data
        
# Load environment variables from a .env file
load_dotenv('secrets_nc.env')

# import inputs
input_dict = json.load(open('inputs_nc.json'))

#Retrieve JSON parsing structure based on metric
parse_dict = json.load(open(input_dict['metrics'] + '.json'))

# main
# build query string + args & urlencode
metric_string = input_dict['metrics'] + '/?limit=' + input_dict['limit']

# send GET resquest to monitoring.powerflex.io
data = get_metrics(metric_string)

# # Parse the JSON response
parsed_data = parse_json_response_nc(data, parse_dict)

# obtain router-specific urls
router_urls = pull_router_url(parsed_data)

# go get the router specifics
router_details = grab_router_details(router_urls, parse_dict)

# combine alert info with router-specific info
parsed_data = combine_alert_with_router(parsed_data, router_details)
print(json.dumps(parsed_data, indent=4))
