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
    
def dump(info):
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)    


def stop_attributes(stops, query):
    #initilize stop id list
    stop_ids=[]
    #iterate through dictionary and add all stop ids to a list
    for stop in stops['data']:
        stop_ids.append(stop[query])
    
    return stop_ids
    
#stop_attributes(get_stops_by_route("Orange"),"id")
    

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
stop_info=get_stop_info(stop_id)
stop_info2=get_stop_predictions(stop_id, "Orange", 1)

# if 'data' in stop_info2:
#     #run through all train predictions
#     for i in range(len(stop_info2['data'])):
#         #get stop info for the index prediction
#         prediction = stop_info2['data'][i]
#         #convert the arrival time to python time
#         time_str = prediction['attributes']['arrival_time']
#         dt = datetime.fromisoformat(time_str)
#         unix_timestamp = int(dt.timestamp())
#         print(f" Train {prediction['relationships']['vehicle']['data']['id']} will arrive at {dt}" )


def turn_on_led(c_stop, led_number ):
    print(f"light at {led_number} is on")


def light_logic(stop_info, vec_list, route, direction):
    #define c_stop route and route from stop_info
    c_stop=stop_info['data']['id']
    
    #get dict from api for predictions for certain stop route and direction
    stop_prediction=get_stop_predictions(c_stop, route, direction)
    
    
    
    #run through all train predictions
    for i in range(len(stop_prediction['data'])):
        prediction = stop_prediction['data'][i]
        train_id = prediction['relationships']['vehicle']['data']['id']
        
        #check if the current train id is in vech list
        if train_id in vec_list:
            print(f"The train {train_id} is accounted for")
            return train_id
        if train_id not in vec_list:
            #get arrive time and convert it to unix
            dt = datetime.fromisoformat(prediction['attributes']['arrival_time'])
            arrive_time = int(dt.timestamp())
            #append current train_id to vech_list
            vec_list.append(train_id)
            #check where train is in comparison with station
            if(arrive_time-current_time<60):
                turn_on_led(c_stop, 1)
            elif(arrive_time - current_time < 180):
                turn_on_led(c_stop, 2)
            else:
                turn_on_led(c_stop, 3)

vec_list=[]
light_logic(stop_info, vec_list, "Orange", 1)




