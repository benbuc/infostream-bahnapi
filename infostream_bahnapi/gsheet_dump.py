import pygsheets
import pandas as pd
from infostream_bahnapi.get_arrivals import get_arrivals
import datetime

LOOKAHEAD = 24  # hours
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# authorization
gc = pygsheets.authorize(service_file="credentials/creds.json")

station_mapping = {
    "Berlin Hbf": "Hbf (Train)",
    "Berlin Südkreuz": "Suedkreuz (Train)",
    "Berlin Ostbahnhof": "Ostbahnhof (Train)",
}

arrival_table = []

arrival_data = get_arrivals(LOOKAHEAD * 60)
all_arrivals = arrival_data["all_arrivals"]
for station in all_arrivals:
    station_name = station["station_name"]
    arrivals = station["arrivals"]
    for arrival in arrivals:
        scheduled = datetime.datetime.fromisoformat(arrival["scheduled"])
        estimated = datetime.datetime.fromisoformat(arrival["estimated"])
        arrival_table.append(
            {
                "Date": scheduled.strftime("%Y-%m-%d"),
                "Time": scheduled.strftime("%H:%M:%S"),
                "ID": arrival["name"],
                "Type": "Train",
                "Bahnhof": station_mapping[station_name],
                "Delay": "true" if arrival["delay"] > 0 else "false",
                "DelayDateTime": estimated.strftime(DATETIME_FORMAT),
                "From": "Origin",
            }
        )

df = pd.DataFrame(arrival_table).sort_values(["Date", "Time"])

sh = gc.open("ua_arrival_times")

wks = sh[0]
wks.set_dataframe(df, (1, 1))
wks.update_value("M1", datetime.datetime.now().strftime(DATETIME_FORMAT))
