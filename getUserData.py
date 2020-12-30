import requests as rs
import pandas as pd
import json
import csv
import os
from datetime import datetime
import time, sys


folder_input = 'output/'
file_path = os.path.join(folder_input, "owner_data.csv") #TODO: Get as commandline input 
csv_data = pd.read_csv(file_path)

partner_output_file_path = "user_data"
user_file_path = os.path.join(folder_input, partner_output_file_path)

def read_from_csv():
    write_to_user_csv()
    try:
        result = read_data_from_csv()
        return result

    except Exception as ex:
        print(ex)


def read_data_from_csv():
    result = csv_data['pretty_id'].unique().tolist()
    # print(len(result))
    for arr in range(0,len(result)):
        # print(result[arr])
        data = post_data(result[arr])
        
        location = data["location"]
        partner = data["partner_info"]["partner_location"]
        image = data["user_avatar"]["jpg_url"]
        print(image)
        write_to_user_csv(data["pretty_id"],data["first_name"],data["last_name_initial"],location["city"],location["region"],location["region_abbreviation"],location["postal_code"],location["country"],location["country_abbreviation"],image,False)
    return result

def post_data(userid):
    try:
        url = 'https://api.twistedroad.com' #base URL
        path = '/api/v1/users/' #get method for API
        headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0','Connection':'keep-alive','Cache-Control':'max-age=0'}
        # values = {'page':vin} #Payload would vary for diffrent APIs
        r = rs.get(url+path+userid,headers=headers)
        return json.loads(r.content.decode('utf-8'))
    except Exception as error:
        print(error)

def write_to_user_csv(pretty_id="",first_name="",last_name_initial="",city="",region="",region_abbreviation="",postal_code="",country="",country_abbreviation="",image="",Is_Header=True ):
        # print(output_file_path)
        try:
            
            with open(user_file_path+'.csv', mode='a') as csv_file:
                    fieldnames = ["pretty_id","first_name","last_name_initial","city","region","region_abbreviation","postal_code","country","country_abbreviation","Image"]
                    writer = csv.writer(csv_file, delimiter=',')
                    if(not Is_Header):
                        csv_data= [pretty_id,first_name,last_name_initial,city,region,region_abbreviation,postal_code,country,country_abbreviation,image]
                        # print(type(csv_data))
                        writer.writerow(csv_data)
                    if(Is_Header):
                            writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass

read_from_csv()