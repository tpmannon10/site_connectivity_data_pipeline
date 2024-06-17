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


def create_band_carrier_lists(full_alarm_dict, metric_dict):
    for label in metric_dict['results'][0].keys():
        full_alarm_dict[label] = []
        for selection in metric_dict['results']:
            full_alarm_dict[label].append(selection[label])
    return full_alarm_dict


def create_metrics_and_alarm_dict(alert_dict, metric_list, time_list):
    full_alarm_dict = {}
    full_alarm_dict["alert_info"] = alert_dict
    for metric in metric_list:
        metric_dict = json.load(open('grafana_metric_' + metric + '.json'))
        if len(metric_dict['results']) > 0:
            full_alarm_dict["cradlepoint_band_carrier"] = metric_dict['results']
            full_alarm_dict = create_band_carrier_lists(full_alarm_dict, metric_dict)
        else:
            values = []
            for item in metric_dict['values']:
                values.append(item[1])
            full_alarm_dict[metric_dict["metric"]] = values
    full_alarm_dict["timesteps"] = time_list
    return full_alarm_dict


def create_full_alert_json(full_alarm_dict, alert_dict):
    full_alarm_dict["date_time"] = str(datetime.now().isoformat(timespec='seconds'))
    filename = alert_dict["acn"] + '-' + alert_dict["acc"] + '_' + alert_dict["type"] + '.json'
    json_object = json.dumps(full_alarm_dict, indent=4)
    with open(filename, 'w') as outfile:
        outfile.write(json_object)
    return

# main
def event_organizer_for_power_bi(alert_dict):
    metric_list = obtain_metric_list('app_configs.json', 'grafana_metric_parser_pair')
    time_list = get_time_metric(json.load(open('grafana_metric_' + metric_list[1] + '.json'))['values'])
    full_alarm_dict = create_metrics_and_alarm_dict(alert_dict, metric_list, time_list)
    create_full_alert_json(full_alarm_dict, alert_dict)
    return
