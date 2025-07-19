import requests
import json
from datetime import datetime

base_url = 'https://api-v3.mbta.com/'

payload = {'filter[route]': 'Orange'}

# Function to get stop information by stop ID
import time

current_time=time.time()

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

#obtain predictions 
def get_stop_predictions(stop_id, route, direction):
    payload = {'filter[stop]' : stop_id, 'filter[route]' : route, 'filter[direction_id]' : direction}
    r = requests.get(f'{base_url}/predictions', params=payload)
    
    if r.status_code == 200:
        return r.json() 
    else: 
        print(f"Failed to retrieve data: {r.status_code}")

stop_id= "place-haecl"
# stop_info=get_stop_predictions(stop_id, "Orange", 1)

# if 'data' in stop_info:
#     #run through all train predictions
#     for i in range(len(stop_info['data'])):
#         #get stop info for the index prediction
#         prediction = stop_info['data'][i]
#         #convert the arrival time to python time
#         time_str = prediction['attributes']['arrival_time']
#         dt = datetime.fromisoformat(time_str)
#         unix_timestamp = int(dt.timestamp())
#         print(f" Train {prediction['relationships']['vehicle']['data']['id']} will arrive at {dt}" )


def turn_on_led(led_number):
    print(f"light at {station} is on")


def light_logic(c_stop, vech_list, route, direction):
    #get dict from api for predictions for certain stop route and direction
    stop_info=get_stop_predictions(c_stop, route, direction)
    prediction = stop_info['data'][i]
    train_id = prediction['relationships']['vechile']['data']['id']
    
    #check if the current train id is in vech list
    if not train_id in vech_list:
        #get arrive time and convert it to unix
        dt = datetime.fromisoformat(prediction['attributes']['arrival_time'])
        arrive_time = int(dt.timestamp())
        if(arrive_time-current_time<60):
            turn_on_led(1)
    else:
        return train_id
    
    
    
    



# with open("output.json", "w", encoding="utf-8") as f:
#     json.dump(stop_info, f, indent=2)


