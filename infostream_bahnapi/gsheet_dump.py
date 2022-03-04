import pygsheets
import pandas as pd
from infostream_bahnapi.get_arrivals import get_arrivals
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

LOOKAHEAD = 24  # hours
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

sheet_mapping = {
    "Date": 0,
    "Time": 1,
    "ID": 2,
    "Type": 3,
    "Bahnhof": 4,
    "IsDelayed": 5,
    "Delay": 6,
    "From": 7,
}

# authorization
gc = pygsheets.authorize(service_file="credentials/creds.json")
logging.info("Authorized Google Sheets Client")

sh = gc.open("ua_arrival_times")
wks = sh[0]
logging.info("Opened Sheet")

current_df = pd.DataFrame(wks)
current_df.columns = current_df.iloc[0]
current_df = current_df[1:]

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
                "IsDelayed": "true" if arrival["delay"] > 0 else "",
                "Delay": estimated.strftime(DATETIME_FORMAT)
                if arrival["delay"] > 0
                else "",
                "From": "Origin",
            }
        )

upcoming_arrivals = pd.DataFrame(arrival_table).sort_values(["Date", "Time"])
new_arrivals = []

# filter out existing arrivals and update delays
for idx, row in upcoming_arrivals.iterrows():
    matching_row = (
        (current_df["Date"] == row["Date"])
        & (current_df["Time"] == row["Time"])
        & (current_df["ID"] == row["ID"])
    )
    if matching_row.any():
        logging.debug(f"Exists: ({row['Time']} - {row['ID']})")
        print(matching_row.idxmax())
    else:
        logging.debug(f"New: ({row['Time']} - {row['ID']})")
        new_arrivals.append(list(row))


# add new arrivals
if new_arrivals:
    wks.update_values((current_df.shape[0] + 2, 1), new_arrivals)

sh[1].update_value("A1", datetime.datetime.now().strftime(DATETIME_FORMAT))
