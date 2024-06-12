import json
from datetime import datetime, timedelta
from dateutil import tz

# convert the alert detected time from UTC timestamp to PST Unix Time
def convert_to_unix_time(date_time_str, window):
    # Remove the portion of the string to the right of the "+" symbol from Netcloud Alert detection timestamp
    date_time_str = date_time_str.split('+')[0]

    # Convert the string to a datetime object
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")

    # Convert the datetime object to PST timezone
    date_time_obj = date_time_obj.replace(tzinfo=tz.gettz('UTC'))
    date_time_obj_pst = date_time_obj.astimezone(tz.gettz('America/Los_Angeles'))

    unix_time = date_time_obj_pst.timestamp()

    time_end = str(unix_time).split('.')[0]
    time_start = str(unix_time_prior(unix_time, window)).split('.')[0]

    return time_start, time_end 

# Subtract 24 hours (in seconds) from the given Unix time
def unix_time_prior(unix_time, window):
    unix_time_prior = unix_time - float(window)*60*60
    return unix_time_prior

# create inputs file for grafana api
def grafana_api_inputs_file(input_dict, out_file_name):
    filename = out_file_name + '.json'
    json_object = json.dumps(input_dict, indent=4)
    with open(filename, 'w') as outfile:
        outfile.write(json_object)
    return

# main
def capture_event_data(event_dict, input_dict, addl_dict):
    # convert unix time and produce time_start and time_end bounds
    input_dict["time_start"], input_dict["time_end"] = convert_to_unix_time(event_dict["detected_at"], addl_dict["time_window_hrs"])
    input_dict["acn"] = event_dict["acn"]
    input_dict["acc"] = event_dict["acc"]

    grafana_api_inputs_file(input_dict, 'inputs')
    return
