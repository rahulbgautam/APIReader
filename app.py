import requests as rs
import time
import os
import csv
import json
              

main_output_file_path = "main_data"
main_output_error_path = "main_error"
image_output_file_path = "image_data"
price_output_file_path = "price_data"
owner_output_file_path ="owner_data"
partner_output_file_path = "partner_data"

folder_input = 'output/'
main_file_path = os.path.join(folder_input, main_output_file_path)
error_output_file_path = os.path.join(folder_input, main_output_error_path)
image_file_path = os.path.join(folder_input, image_output_file_path)
price_file_path  = os.path.join(folder_input, price_output_file_path)
owner_file_path = os.path.join(folder_input, owner_output_file_path)
partner_file_path = os.path.join(folder_input, partner_output_file_path)
def post_vin(vin):
    try:
        #/usr/local/bin/python3
        #'https://api.twistedroad.com/api/v1/motorcycles/search'
        # page=3
       # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        server = 'ievm'
        
        url = 'https://api.twistedroad.com' #base URL
        path = '/api/v1/motorcycles/search' #get method for API
        headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0','Connection':'keep-alive','Cache-Control':'max-age=0'}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_indx
        values = {'page':vin} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content.decode('utf-8'))
    except Exception as error:
        print(error)

def jsonify_result(df):
    new_str = df.decode('utf-8') # Decode using the utf-8 encoding
    # return json.loads(new_str.to_json(orient='records'))
    return json.dumps(new_str)

def readData():
    # List of Vins
    # result = read_from_csv()
    call_vin_decode()

def call_vin_decode():
    write_to_main_csv()
    write_to_error_csv()
    write_to_image_csv()
    write_to_pricing_csv()
    write_to_owner_csv()
    write_to_partner_csv()
    try:
        i=1
        filNum =1
        page_num = 147
        for vin in range(0,page_num):
             
            vin_data = post_vin(vin)
            # print("body_data:",vin_data["Body"])
            if len(vin_data["Body"]) > 0:
                body_data = vin_data["Body"][0]
                bbdatafin = getBBData(vin,body_data['Model_Year'],body_data['Make'],body_data['Model'],body_data['Series_Name'])
                wholeacv = (bbdatafin[0])
                retailacv = (bbdatafin[1])

                write_to_csv(vin,body_data['Model_Year'],body_data['Make'],body_data['Model'],body_data['Salvage_Type'],body_data['Body_Style_Name'],body_data['Series_Name'],body_data['EngineInformation'],body_data['Cylinders'],body_data['Fuel_Type'],body_data['Base_Shipping_Weight'],body_data['CountryOfOrigin'],body_data['Segmentation_Description'],body_data['Transmission_Type_Description'],body_data['TransmissionSpeed'],wholeacv,retailacv,False)
            else:
                write_to_error_csv(vin,False)
            # print(type(body_data['Model_Year']))
            # if(i == 200):
            #    filNum = filNum +1
            #    i = 0
            #    output_file_path = output_file_path +"_"+str(filNum)
            #    error_output_file_path = error_output_file_path+"_"+str(filNum)
            i=i+1
    except Exception as error:
        print(error)
        pass
    
def getBBData(vin,year,make,model,series):

    bbdata = post_BB(vin,year,make,model,series)
    wholeacv = 0
    retailacv = 0
    if len(bbdata["Body"]) > 0:
        body_data = bbdata["Body"][0]
        wholeacv = body_data['WholeACV']
        retailacv = body_data['RetailACV']
    return wholeacv,retailacv

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

def write_to_csv(vin="", modelyear="", makename="", modelname="", salvagetype="", bodystylename="", seriesname="", EngineInformation="", cylinders="", FuelTypeDescription="", BaseShippingWeight="", CountryOfOrigin="", SegmentationDescription="", TransmissionDescription="", TransmissionSpeed="", BlackBookWACVValue ="",BlackBookRACVValue ="", Is_Header=True ):
        # print(output_file_path)
        with open(output_file_path+".csv", mode='a',newline='') as csv_file:
                fieldnames = ["vin","modelyear","makename","modelname","salvagetype","bodystylename","seriesname","EngineInformation","cylinders","FuelTypeDescription","BaseShippingWeight","CountryOfOrigin","SegmentationDescription","TransmissionDescription","TransmissionSpeed","BlackBook Whole ACV","BlackBook Retail ACV"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [vin , modelyear , makename , modelname , salvagetype , bodystylename , seriesname , EngineInformation , cylinders , FuelTypeDescription , BaseShippingWeight , CountryOfOrigin , SegmentationDescription , TransmissionDescription , TransmissionSpeed , BlackBookWACVValue,BlackBookRACVValue]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass

            


def write_to_pricing_csv(data_id="",discount_days="",discount_percent="",Is_Header=True ):
        # print(output_file_path)
        try:
            with open(price_file_path+'.csv', mode='a') as csv_file:
                fieldnames = ["data_id","discount_days","discount_percent"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [data_id,discount_days,discount_percent]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass
def write_to_owner_csv(data_id="",owner_id="",pretty_id="",uuid="",user_id="",state="",first_name="",last_name_initial="",Is_Header=True ):
        # print(output_file_path)
        try:
            with open(owner_file_path+'.csv', mode='a') as csv_file:
                fieldnames = ["data_id","owner_id","pretty_id","uuid","user_id","state","first_name","last_name_initial"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [data_id,owner_id,pretty_id,uuid,user_id,state,first_name,last_name_initial]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass
        
def write_to_partner_csv(data_id="",partner_type="",partner_name="",partner_parent_company="",partner_inventory_count="",partner_banner="",Is_Header=True ):
        # print(output_file_path)
        try:
            with open(partner_file_path+'.csv', mode='a') as csv_file:
                fieldnames = ["data_id","partner_type","partner_name","partner_parent_company","partner_inventory_count","partner_banner"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [data_id,partner_type,partner_name,partner_parent_company,partner_inventory_count,partner_banner]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass

def write_to_error_csv(vin="",Is_Header=True ):
        # print(output_file_path)
        try:
            with open(error_output_file_path+".csv", mode='a') as csv_file:
                fieldnames = ["id"]                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [vin]
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                    writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass


readData()