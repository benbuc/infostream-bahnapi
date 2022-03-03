from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import datetime
import json
import cachetools.func
import pytz


def is_station_of_interest(station):
    return station.name in ["Berlin Hbf", "Berlin Ostbahnhof", "Berlin Südkreuz"]


def is_arrival_of_interest(arrival):
    return True
    return "IC" in arrival.name


def get_arrivals(duration=15):
    client = HafasClient(DBProfile())

    stations = [
        station
        for station in client.locations("Berlin")
        if is_station_of_interest(station)
    ]

    all_arrivals = []
    print(datetime.datetime.now().isoformat())
    for station in stations:
        arrivals_of_interest = [
            arrival
            for arrival in client.arrivals(
                station=station,
                date=datetime.datetime.now(tz=pytz.timezone("Europe/Berlin")),
                duration=duration,
            )
            if is_arrival_of_interest(arrival)
        ]
        arrivals_for_station = []
        for arrival in arrivals_of_interest:
            arrival_dict = {
                "name": arrival.name,
                "scheduled": arrival.dateTime.isoformat(),
                "platform": arrival.platform,
            }
            if arrival.delay:
                arrival_dict["estimated"] = (
                    arrival.dateTime + arrival.delay
                ).isoformat()
                arrival_dict["delay"] = arrival.delay.seconds
            else:
                arrival_dict["estimated"] = arrival_dict["scheduled"]
                arrival_dict["delay"] = 0

            arrivals_for_station.append(arrival_dict)

        all_arrivals.append(
            {"station_name": station.name, "arrivals": arrivals_for_station}
        )

    return {
        "all_arrivals": all_arrivals,
        "last_update": datetime.datetime.now(),
    }


@cachetools.func.ttl_cache(maxsize=128, ttl=60)
def get_cached_arrivals():
    return get_arrivals()


if __name__ == "__main__":
    get_arrivals()
