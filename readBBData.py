import requests as rs
import time
import os
import csv
from dataaccess import read_from_csv,read_bbdata_from_csv,folder_input,init_csv
import json

folder_output = 'output/'
output_file_path = os.path.join(folder_output, init_csv("BBData_output"))
error_output_file_path = os.path.join(folder_output, init_csv("BBData_Error"))

import csv

filename = 'input/sample_bb.csv'


def readData():
    # List of Vins
    write_to_csv()
    write_to_error_csv()

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        i=0
        for row in datareader:
            if(i>690408):
                processRow(row)
            i = i+1
            print(i)

def processRow(row):
    # print(row[4])
    trim_source =''
    IHS_Trim = getIHSTrim(row[0])
    if(row[8] == '0'):
        # IHS_Trim = getIHSTrim(row[0])
        trim_source = 'IHS'
    else:
        IHS_Trim = row[4]
        trim_source = 'CHROME'
    vin = row[0]
    year = row[1]
    make = row[2]
    model= row[3]
    series= IHS_Trim
    best_trim = IHS_Trim

    bbdatafin = getBBData(vin,year,make,model,series)
    bbdatafinvin = getBBData(vin,year,make,model,series,vin)
    wholeacv = (bbdatafin[0])
    retailacv = (bbdatafin[1])
    write_to_csv(vin,year,make,model,row[4],IHS_Trim,best_trim,trim_source,row[8],row[9],row[10],wholeacv,retailacv,False)



def getBBData(vin,year,make,model,series):

    bbdata = post_BB(vin,year,make,model,series)
    wholeacv = 0
    retailacv = 0
    if len(bbdata["Body"]) > 0:
        body_data = bbdata["Body"][0]
        wholeacv = body_data['WholeACV']
        retailacv = body_data['RetailACV']
    return wholeacv,retailacv


def getBBDataVIN(vin,year,make,model,series):

    bbdata = post_BB_VIN(vin,year,make,model,series)
    wholeacv = 0
    retailacv = 0
    if len(bbdata["Body"]) > 0:
        body_data = bbdata["Body"][0]
        wholeacv = body_data['WholeACV']
        retailacv = body_data['RetailACV']
    return wholeacv,retailacv

def getIHSTrim(vin):
    vin_data = post_vin(vin)
    # print(vin_data)
    if len(vin_data["Body"]) > 0:
        body_data = vin_data["Body"][0]
        return body_data['Series_Name'] 
    return ''
    # IHSTrim = 
def post_vin(vin):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        server = 'ievm'
        url = 'http://'+server+'.iaai.com' #base URL
        path = '/api/iaadecodevin' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd'}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = {'vin':vin,'FullDetails':1,'vendor':'IHS'} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)


def post_BB(vin,year,make,model,series):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        

        server = 'ievm'
        url = 'http://'+server+'.iaai.com' #base URL
        path = '/api/vehiclevaluations' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd','Content-Type':'application/json'}
   
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = { 'vehicles':[{
                       
                        'vin':vin,
                        'year':year,
                        'make':make,
                        'model':model,
                        'series':series,
                       
                     
                    }
                ],
                "forceAPICheck":'true'
                }

        # {'vin':vin,'FullDetails':1,'vendor':'IHS'} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.post(url+path,headers=headers,data=json.dumps(values))
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

def post_BB_VIN(vin,year,make,model,series):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        

        server = 'ievm'
        url = 'http://'+server+'.iaai.com' #base URL
        path = '/api/vehiclevaluations' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd','Content-Type':'application/json'}
   
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = { 'vehicles':[{
                       
                        'vin':vin,
                    }
                ],
                "forceAPICheck":'true'
                }

        # {'vin':vin,'FullDetails':1,'vendor':'IHS'} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.post(url+path,headers=headers,data=json.dumps(values))
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

def write_to_csv(VIN="",Year="",Make="",Model="",Trim_Chrome="",Trim_IHS="",Trim_Best="",Trim_Source="",Build_Ind="",MSRP_Low_Chrome="",MSRP_High_Chrome="",Wholesale_Price_BlackBook="",Retail_Price_BlackBook = "", Is_Header=True ):
        # print(output_file_path)
        with open(output_file_path+".csv", mode='a',newline='') as csv_file:
                fieldnames = ['VIN','Year','Make','Model','Trim Chrome','Trim IHS','Trim Best','Trim Source','Build Ind','MSRP Low Chrome','MSRP High Chrome','Wholesale Price BlackBook','Retail Price BlackBook']
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [VIN,Year,Make,Model,Trim_Chrome,Trim_IHS,Trim_Best,Trim_Source,Build_Ind,MSRP_Low_Chrome,MSRP_High_Chrome,Wholesale_Price_BlackBook,Retail_Price_BlackBook]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)

def write_to_error_csv(vin="",Is_Header=True ):
        # print(output_file_path)
        with open(error_output_file_path+".txt", mode='a',newline='') as csv_file:
                fieldnames = ["vin"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [vin]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
readData()
