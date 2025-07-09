import requests
import json

base_url = 'https://api-v3.mbta.com/'

payload = {'filter[route]': 'Orange'}

# Function to get stop information by stop ID


def get_stops_by_route(route):
    payload = {'filter[route]' : route}
    r = requests.get(f'{base_url}/stops', params=payload)
    data = r.json()
    print(json.dumps(data, indent=2))  # Pretty print
    return data
    
    
get_stops_by_route("Orange")
    

def get_stop_info(stop_id):
    r = requests.get(f'https://api-v3.mbta.com/stops/{stop_id}')
    
    if r.status_code == 200:
        return r.json() 
    else: 
        print(f"Failed to retrieve data: {r.status_code}")

stop_id= "70025"
stop_info=get_stop_info(stop_id)

#if stop_info:
#    print(f"Name: {stop_info['data']['attributes']['name']}")
