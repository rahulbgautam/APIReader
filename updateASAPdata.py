import requests as rs
import time
import os
import csv
from dataaccess import read_from_csv,read_bbdata_from_csv,folder_input,init_csv
import json
import datetime

folder_output = 'output/'
output_file_path = os.path.join(folder_output, init_csv("ASAPData_output"))
error_output_file_path = os.path.join(folder_output, init_csv("ASAPData_Error"))

import csv

filename = 'input/Data_PROD_06022021.csv'



def readData():
    # List of Vins
    write_to_csv()
    write_to_error_csv()

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        i=0
        print('Date started' , datetime.datetime.now() )
        for row in datareader:
            if(i>316214):
                processRow(row)
            i = i+1
            print(i)
        print('Date endded' , datetime.datetime.now() )

def processRow(row):
    # print(row[4])
    trim_source =''
    
    salvage_id = row[0]
    vin = row[1]
    
    bbasapdatafinvin = getChromeDataVIN(vin)
    # print(bbasapdatafinvin)
    # wholeacv = (bbdatafinvin[0])
    # retailacv = (bbdatafinvin[1])
    Length = (bbasapdatafinvin[0])
    Height = (bbasapdatafinvin[1])
    Width = (bbasapdatafinvin[2])
    Weight = (bbasapdatafinvin[3])
    MSRPBuilt = (bbasapdatafinvin[4])
    MSRPLow = (bbasapdatafinvin[5])
    MSRPHigh = (bbasapdatafinvin[6])
    BuiltInd = (bbasapdatafinvin[7])
    BuiltDate = (bbasapdatafinvin[8])
    Displ_Liters = (bbasapdatafinvin[9])
    write_to_csv(salvage_id,vin,Length,Height,Width,Weight,MSRPBuilt,MSRPLow,MSRPHigh,BuiltInd,BuiltDate,Displ_Liters,False)

def getChromeDataVIN(vin):

    bbdata = post_CHROME_VIN(vin)
    # print(bbdata)
    Length = ''
    Height = ''
    Width = ''
    Weight = ''
    MSRPBuilt = ''
    MSRPLow = ''
    MSRPHigh = ''
    BuiltInd = ''
    BuiltDate = ''
    Displ_Liters = ''
    if len(bbdata["Body"]) > 0:
        body_data = bbdata["Body"][0]
        Length = body_data['Length']
        Height = body_data['Height']
        Width = body_data['Width']
        Weight  = body_data['Weight']
        MSRPBuilt = body_data['MSRPBuilt']
        MSRPLow = body_data['MSRPLow']
        MSRPHigh = body_data['MSRPHigh']
        BuiltInd = body_data['BuiltInd']
        BuiltDate = body_data['BuiltDate']
        Displ_Liters = body_data['Displ_Liters']

    return Length,Height,Width,Weight,MSRPBuilt,MSRPLow,MSRPHigh,BuiltInd,BuiltDate,Displ_Liters


def post_CHROME_VIN(vin):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        server = 'evm'
        url = 'https://'+server+'.iaai.com' #base URL
        path = '/api/iaadecodevin' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd'}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = {'vin':vin,'FullDetails':1} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        write_to_error_csv(vin=vin,Is_Header=False )
        print(error)

def post_BB_VIN(vin,year,make,model,series):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        

        server = 'evm'
        url = 'https://'+server+'.iaai.com' #base URL
        path = '/api/vehiclevaluations' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd','Content-Type':'application/json'}
   
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = { 'vehicles':[{
                       
                        'vin':vin,
                    }
                ],
                "forceAPICheck":'false'
                }

        # {'vin':vin,'FullDetails':1,'vendor':'IHS'} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.post(url+path,headers=headers,data=json.dumps(values))
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        write_to_error_csv(vin=vin,Is_Header=False )
        print(error)

def write_to_csv(SalvageID="",VIN="",Length="",Height="",Width="",Weight="",MSRPBuilt="",MSRPLow="",MSRPHigh="",BuiltInd="",BuiltDate="",Displ_Liters="", Is_Header=True ):
        # print(output_file_path)
        with open(output_file_path+".csv", mode='a',newline='') as csv_file:
                fieldnames = ['SalvageID','VIN','Length','Height','Width','Weight','MSRPBuilt','MSRPLow','MSRPHigh','BuiltInd','BuiltDate','Displ_Liters']
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [SalvageID,VIN,Length,Height,Width,Weight,MSRPBuilt,MSRPLow,MSRPHigh,BuiltInd,BuiltDate,Displ_Liters]
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