from datetime import datetime
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

# create filtered alerts file
def filtered_alerts_file(relevant_alerts, out_file_name):
    relevant_alerts["date_time"] = datetime.now().isoformat(timespec='seconds')
    filename = out_file_name + '.json'
    json_object = json.dumps(relevant_alerts, indent=4)
    with open(filename, 'w') as outfile:
        outfile.write(json_object)
    return

# take in latest alerts
alerts = open_alerts('nc_alerts_update.json')

# obtain alert filter
alert_filter = open_alerts('alert_filter.json')

# filter out relevant alerts
relevant_alerts = alert_filtering(alerts, alert_filter)

# output filtered alerts list in json file
filtered_alerts_file(relevant_alerts, 'filtered_alerts')


