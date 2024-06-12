from datetime import datetime
import json
# import pandas as pd

# take in grafana metrics & info for a given alert, convert the data into something ingestible by PowerBI then send to PowerBI dashboard

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

metric_dict = json.load(open('grafana_metric_cradlepoint_rsrp.json'))

print(json.dumps(metric_dict, indent=4))
