import googlemaps
import urllib
import json
from datetime import datetime, timedelta

# insert key - must be obtained from google
key = ''


# Initialise 
print("===========================")
print("Travel Times by Pavel Hošek")
print("===========================")
print("using Google Maps planner to estimate travel times to various locations")
#now = datetime.now()
now = datetime.fromisoformat('2023-11-20T07:00:00')
gmaps = googlemaps.Client(key=)
origin = "Pankrác"


# load PID stops
with urllib.request.urlopen("https://data.pid.cz/stops/json/stops.json") as url:
    stops = json.load(url)
    times = {}
    for stop in stops["stopGroups"]:
        if stop['name'] == origin:
            originLatLon = f"{stop['avgLat']},{stop['avgLon']}"
            break

    for delta in [0]: #range(0,0,0):
        #i = 0
        for stop in stops["stopGroups"]:
            if stop['municipality'] == "Praha" and stop['name'] != origin:
                directions_result = gmaps.directions(
                    originLatLon, f"{stop['avgLat']},{stop['avgLon']}", mode="transit", departure_time = now + timedelta(minutes=delta))
                travelTime = directions_result[0]['legs'][0]['duration']['value']
                if stop['name'] not in times.keys():
                    times[stop['name']] = round(travelTime/60) 
                if times[stop['name']] > round(travelTime/60):
                    times[stop['name']] = round(travelTime/60) 
                print(f"{stop['name']}; {now + timedelta(minutes=delta)}; {round(travelTime/60)}; {times[stop['name']]}")
            #i += 1
            #if i > 3:
            #    break            

            
    #i = 0
    f = open("output.csv", "w")
    f.write(f"Stop Name; LatLon; Time [min]\n")
    for stop in stops["stopGroups"]:
        if stop['municipality'] == "Praha" and stop['name'] != origin:
            f.write(f"{stop['name']}; {stop['avgLat']},{stop['avgLon']}; {times[stop['name']]}\n")            
        #i += 1
        #if i > 3:
        #    break              
    f.close()
