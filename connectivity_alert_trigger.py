import requests
from urllib.parse import urlencode
from datetime import datetime
import os
import json

# open alert output json
def open_alerts(alert_output_file):
    return json.load(open(alert_output_file))

# filter out alert results
def alert_filtering(alerts, filter):
    relevant_alerts = {"alerts": []}
    for item in alerts["data"]:
        if item["type"] in filter['alert_list']:
            relevant_alerts["alerts"].append(item)
    return relevant_alerts

# take in latest alerts
alerts = open_alerts('nc_alerts_update.json')
print(json.dumps(alerts, indent= 4))

# obtain alert filter
alert_filter = open_alerts('alert_filter.json')

# filter out relevant alerts
relevant_alerts = alert_filtering(alerts, alert_filter)
print(json.dumps(relevant_alerts, indent= 4))


