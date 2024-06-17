from datetime import datetime
import json
from event_data_capture import capture_event_data
from api_connector_grafana import grafana_api_connect
from event_organizer import event_organizer_for_power_bi

# create the inputs for the grafana event data capture
def create_input_dict(app_config_dict):
    input_dict = app_config_dict["grafana_api_input_keys"]
    for item in app_config_dict["grafana_api_addl"].keys():
        if item in input_dict.keys():
            input_dict[item] = app_config_dict["grafana_api_addl"][item]
    return input_dict


# bring in app configs
app_configs = json.load(open('app_configs.json'))

# Kick off the alert query for Netcloud


# filter the results


# pull in filtered results and initiate grafana queries if necessary
filtered_alerts = json.load(open('filtered_alerts.json'))
if len(filtered_alerts["alerts"]) > 0:
    input_dict = create_input_dict(app_configs)
    for alert in filtered_alerts["alerts"]:
        for metric in app_configs["grafana_metric_parser_pair"].keys():
            input_dict["metrics"] = metric
            input_dict["parse_profile"] = app_configs["grafana_metric_parser_pair"][metric]
            capture_event_data(alert, input_dict, app_configs["grafana_api_addl"])
            grafana_api_connect()
        event_organizer_for_power_bi(alert)
