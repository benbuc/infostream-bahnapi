from pyhafas import HafasClient
from pyhafas.profile import DBProfile
import datetime
import json
import cachetools.func


def is_station_of_interest(station):
    return station.name in ["Berlin Hbf", "Berlin Ostbahnhof", "Berlin Südkreuz"]


def is_arrival_of_interest(arrival):
    return "IC" in arrival.name


def get_arrivals():
    client = HafasClient(DBProfile())

    stations = [
        station
        for station in client.locations("Berlin")
        if is_station_of_interest(station)
    ]

    all_arrivals = {}
    for station in stations:
        arrivals_of_interest = [
            arrival
            for arrival in client.arrivals(
                station=station, date=datetime.datetime.now(), duration=15
            )
            if is_arrival_of_interest(arrival)
        ]
        all_arrivals[station.name] = []
        for arrival in arrivals_of_interest:
            all_arrivals[station.name].append(
                {
                    "name": arrival.name,
                    "scheduled": arrival.dateTime.isoformat(),
                    "estimated": (arrival.dateTime + arrival.delay).isoformat(),
                    "delay": arrival.delay.seconds,
                }
            )

    return all_arrivals


@cachetools.func.ttl_cache(maxsize=128, ttl=60)
def get_cached_arrivals():
    return get_arrivals()
