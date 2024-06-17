from datetime import datetime
import json
# import pandas as pd

# take in grafana metrics & info for a given alert, convert the data into something ingestible by PowerBI then send to PowerBI dashboard

def obtain_metric_list(config_filename, json_list_key): 
    metric_keys = json.load(open('app_configs.json'))['grafana_metric_parser_pair'].keys()
    metric_list = []
    for item in metric_keys:
        metric_list.append(item)
    return metric_list


def convert_unix_to_date_time(unix_time):
    dt = datetime.fromtimestamp(int(unix_time))
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def get_time_metric(time_dict):
    time_list = []
    for item in time_dict:
        time_list.append(convert_unix_to_date_time(item[0]))
    return time_list


def create_metrics_and_alarm_dict(alert_dict, metric_list, time_list):
    full_alarm_dict = {}
    full_alarm_dict["alert_info"] = alert_dict
    for metric in metric_list:
        metric_dict = json.load(open('grafana_metric_' + metric + '.json'))
        if len(metric_dict['results']) > 0:
            full_alarm_dict["cradlepoint_band_carrier"] = metric_dict['results']
        else:
            values = []
            for item in metric_dict['values']:
                values.append(item[1])
            full_alarm_dict[metric_dict["metric"]] = values
    full_alarm_dict["timesteps"] = time_list
    return full_alarm_dict


alert_dict = {
            "created_at": "2024-06-11T17:58:24.249477+00:00",
            "created_at_timeuuid": "3274f130-281c-11ef-bcba-3674ac214bf2",
            "detected_at": "2024-06-11T17:58:09+00:00",
            "friendly_info": "The Internal 150M-D (SIM1) mdm on port Internal 1 has connected to the network.",
            "type": "modem_wan_connected",
            "router": "https://www.cradlepointecm.com/api/v2/routers/3659485/",
            "description": "pf-0119-03 Rydell Northridge 010-2190",
            "name": "IBR600C-41d",
            "state": "online",
            "state_updated_at": "2024-06-11T17:58:18.918550+00:00",
            "acn": "0119",
            "acc": "03"
        }


metric_list = obtain_metric_list('app_configs.json', 'grafana_metric_parser_pair')
print(metric_list)

time_list = get_time_metric(json.load(open('grafana_metric_' + metric_list[1] + '.json'))['values'])
print(time_list)

full_alarm_dict = create_metrics_and_alarm_dict(alert_dict, metric_list, time_list)
print(json.dumps(full_alarm_dict, indent=4))
