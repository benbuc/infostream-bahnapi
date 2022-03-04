import pygsheets
import pandas as pd
from infostream_bahnapi.get_arrivals import get_arrivals
import datetime

LOOKAHEAD = 24  # hours
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# authorization
gc = pygsheets.authorize(service_file="credentials/creds.json")

# column_mapping = [
#    ("Status", 2),
#    ("Date", 3),
#    ("Time", 4),
#    ("Type", 5),
#    ("Station", 6),
#    ("ID", 7),
#    ("Description / Legend", 10),
# ]

station_mapping = {
    "Berlin Hbf": "Hbf (Train)",
    "Berlin Südkreuz": "Suedkreuz (Train)",
    "Berlin Ostbahnhof": "Ostbahnhof (Train)",
}

# Create empty dataframe
# df = pd.DataFrame(columns=[c[0] for c in column_mapping])
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

df = pd.DataFrame(arrival_table)

sh = gc.open("ua_arrival_times")
wks = sh[0]

# update the first sheet with df, starting at cell B2.
print(df)

# for mapping in column_mapping:
wks.set_dataframe(df, (1, 1))
wks.update_value("M1", datetime.datetime.now().strftime(DATETIME_FORMAT))

# for mapping in column_mapping:
#    wks.set_dataframe(df.filter([mapping[0]]), (1, mapping[1]))
