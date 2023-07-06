import pandas as pd
import json
import csv
import os
from datetime import datetime
import time, sys


folder_input = 'input/'
file_path = os.path.join(folder_input, "RB_VIN_DATA.csv") #TODO: Get as commandline input 


csv_data = pd.read_csv(file_path)

def init_csv(output_csv):
        now  = datetime.now()
        date_time = now.strftime("_%m%d%Y%H%M%S")
        output_version = output_csv + date_time
        return output_version

def authenticate(header):
    print(header)
    auth = header.get("X-Api-Key")
    print(auth,"=",auth)
    if auth == 'eiWee8ep9due4deeshoa8Peichai8Eih':
        return True
    else:
        return False

def read_from_csv():
    try:
        result = read_vin_from_csv()
        return result

    except Exception as ex:
        print(ex)

def read_bbdata_from_csv():
    result = csv_data
    #print(result)
    # result = jsonify_result(result)
    return result


def read_vin_from_csv():
    result = csv_data['VIN'].unique().tolist()
    # print(result)
    # result = jsonify_result(result)
    return result

# Returns a list of cities matching a pattern        
def read_city_from_csv(city):
    if city != None:
        result = csv_data[csv_data['City'].str.startswith(city.upper())] 
    else:
        return csv_data['City'].unique().tolist()
    result = result['City'].unique().tolist()
    # print(result)
    # result = jsonify_result(result)
    return result

def read_city_from_state(state):
    if state != None:
        result = csv_data[csv_data['State'].str.startswith(state.upper())]
        
    else:
        return csv_data['City'].unique().tolist()
    result = result.sort_values(['City'], ascending = (True)) 
    result = result['City'].unique().tolist()
    # print(result)
    # result = jsonify_result(result)
    return result

# Returns a list of states matching a pattern        
def read_state_from_csv(state):
    if state != None:
        result = csv_data[csv_data['State'].str.startswith(state.upper())] 
    else:
        return csv_data['State'].unique().tolist()
    result = result['State'].unique().tolist()
    # print(result)
    # result = jsonify_result(result)
    return result

def read_city_data(city):
    result = csv_data[csv_data['City'].str.contains(city.upper())] 
    result = jsonify_result(result)
    print(len(result))
    if(len(result) > 0):
        return result
    return result

def read_state_data(state):
    result = csv_data.loc[(csv_data['State'] == state)]
    result = jsonify_result(result)
    print(len(result))
    if(len(result) > 0):
        return result
    return result

def read_state_city_data(state,city):
    if state == None:
        result = csv_data.loc[csv_data['City'].str.startswith(city.upper())]
    else:    
        result = csv_data.loc[(csv_data['State'] == state.upper()) & csv_data['City'].str.contains(city.upper())]
    
    result = jsonify_result(result)
    # print(result)
    if(len(result) > 0):
        return result

    return result

def jsonify_result(df):
    return json.loads(df.to_json(orient='records'))
if __name__ == "__main__":
    print(read_city_from_csv("chicago"))
    