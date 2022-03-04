import pygsheets
import pandas as pd
from infostream_bahnapi.get_arrivals import get_arrivals

# authorization
gc = pygsheets.authorize(service_file="credentials/creds.json")

column_mapping = [
    ("Status", 2),
    ("Date", 3),
    ("Time", 4),
    ("Type", 5),
    ("Station", 6),
    ("ID", 7),
    ("Description / Legend", 10),
]

# Create empty dataframe
# df = pd.DataFrame(columns=[c[0] for c in column_mapping])
arrival_table = []

arrival_data = get_arrivals(8 * 60)
all_arrivals = arrival_data["all_arrivals"]
for station in all_arrivals:
    station_name = station["station_name"]
    arrivals = station["arrivals"]
    for arrival in arrivals:
        arrival_table.append(
            {
                "Date": arrival["scheduled"],
                "Station": station_name,
                "ID": arrival["name"],
            }
        )

df = pd.DataFrame(arrival_table)

sh = gc.open("ua_arrival_times")
wks = sh[0]

# update the first sheet with df, starting at cell B2.
print(df)

# for mapping in column_mapping:
# wks.set_dataframe(df, (1, 1))

for mapping in column_mapping:
    wks.set_dataframe(df.filter([mapping[0]]), (1, mapping[1]))
