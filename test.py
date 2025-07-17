import requests
import json

base_url = 'https://api-v3.mbta.com/'

payload = {'filter[route]': 'Orange'}

# Function to get stop information by stop ID


def get_stops_by_route(route):
    payload = {'filter[route]' : route}
    r = requests.get(f'{base_url}/stops', params=payload)
    stops = r.json()
    #print(json.dumps(stops, indent=2))  # Pretty print
    return stops
    
    
#get_stops_by_route("Orange")

def stop_attributes(stops, query):
    #initilize stop id list
    stop_ids=[]
    #iterate through dictionary and add all stop ids to a list
    for stop in stops['data']:
        stop_ids.append(stop[query])
    
    return stop_ids
    
stop_attributes(get_stops_by_route("Orange"),"id")
    

def get_stop_info(stop_id):
    r = requests.get(f'https://api-v3.mbta.com/stops/{stop_id}')
    
    if r.status_code == 200:
        return r.json() 
    else: 
        print(f"Failed to retrieve data: {r.status_code}")


def get_stop_predictions(stop_id, route, direction):
    payload = {'filter[stop]' : stop_id, 'filter[route]' : route, 'filter[direction_id]' : direction}
    r = requests.get(f'{base_url}/predictions', params=payload)
    
    if r.status_code == 200:
        return r.json() 
    else: 
        print(f"Failed to retrieve data: {r.status_code}")

stop_id= "place-haecl"
stop_info=get_stop_predictions(stop_id, "Orange", 1)

if 'data' in stop_info:
    for i in range(min(3, len(stop_info['data']))):
        prediction = stop_info['data'][i]
        print(prediction['attributes']['arrival_time'])

#print(stop_info)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(stop_info, f, indent=2)

