import requests as rs
import time
import os
import csv
import json
from dataaccess import read_from_csv,read_bbdata_from_csv,folder_input,init_csv
from generate_token import generateHashDigest
main_output_file_path = "main_data"
main_output_error_path = "main_error"
image_output_file_path = "image_data"
price_output_file_path = "price_data"
owner_output_file_path ="owner_data"
partner_output_file_path = "partner_data"

folder_output = 'output/'
output_file_path = os.path.join(folder_output, init_csv("CVD_Data_output"))
error_output_file_path = os.path.join(folder_output, init_csv("CVD_Data_Error"))

def post_vin_to_cvd(vin):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JF1GH63619H827603' #'JAFSR175LDM465808'
        server = 'ievm'
        url = 'https://cvd.api.chromedata.com:443/v1.0/CVD/vin/' #base URL
        path = vin #get method for API
        token = generateHashDigest()
        headers ={'Content-Type':'application/json','Accept':'application/json','Authorization':token}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        # values = {'vin':vin,'FullDetails':1} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print("post_vin_to_cvd:",error)


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
        values = {'vin':vin,'FullDetails':1} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

def jsonify_result(df):
    new_str = df.decode('utf-8') # Decode using the utf-8 encoding
    # return json.loads(new_str.to_json(orient='records'))
    return json.dumps(new_str)

def readData():
    # List of Vins
    result = read_from_csv()
    call_vin_decode(result)

def call_vin_decode(data):
    write_to_csv()
    write_to_error_csv()
    # write_to_image_csv()
    # write_to_pricing_csv()
    # write_to_owner_csv()
    # write_to_partner_csv()
    try:
        i=1
      
        filNum =1
        page_num = 147
        for vin in data:
            # if i > 0:
            print(vin)
            # vin ='1GCHG35U741219078'
            vin_data = post_vin_to_cvd(vin)
           
            if vin_data["error"] == True:
                continue
           
            body_data = vin_data["result"]
            

            engine_data = list(filter(lambda x:x["id"]=="21670",body_data["features"]))
            engine_info =''
            if engine_data:
                if 'name' in engine_data[0]:
                    engine_info =engine_data[0]['name']
            # print(engine_info)


            cylinder_data = list(filter(lambda x:x["id"]=="21691",body_data["techSpecs"]))
            cylinder_info=''
            if cylinder_data:
                if 'name' in cylinder_data[0]:
                    cylinder_info =cylinder_data[0]['name']
            
            fuel_data = list(filter(lambda x:x["id"]=="10030",body_data["features"]))
            fuel_info=''
            if fuel_data:
                if 'name' in fuel_data[0]:
                    fuel_info =fuel_data[0]['name']
            # print(fuel_info)
            # print("body_data:",body_data["features"][0])
            drive_data = list(filter(lambda x:x["id"]=="10750",body_data["features"]))
            drive_type=''
            if drive_data:
                if 'name' in drive_data[0]:
                    drive_type=drive_data[0]['name']
            # print(len(drive_data))
            # weight_data = list(filter(lambda x:x["id"]=="22160",body_data["techSpecs"]))
            # if 'name' in weight_data[0]:
            #     curb_weight=weight_data[0]['name']    
            
            transmission_data = list(filter(lambda x:x["id"]=="10500",body_data["features"]))
            transmission_type= ''
            if transmission_data:
                if 'name' in transmission_data[0]:
                    transmission_type=transmission_data[0]['name']

            # print(transmission_type)

            # vehicle_data_1 = list(filter(lambda x:x["styleId"]==10260,body_data["vehicles"]))
            vehicle_data_1 =body_data["vehicles"]
            style_name =''
            if 'styleDescription' in vehicle_data_1[0]:
                style_name =vehicle_data_1[0]['styleDescription']
            country_of_origin =''
            if 'country' in vehicle_data_1[0]:
                country_of_origin = vehicle_data_1[0]['country']
            
            segment = ''
            if 'segment' in vehicle_data_1[0]:
                segment = vehicle_data_1[0]['segment'][0]
            drive_Type =''
            if 'driveType' in vehicle_data_1[0]:
                drive_Type = vehicle_data_1[0]['driveType']
            # vehicle_data_2 = list(filter(lambda x:x["styleId"]==10261,body_data["vehicles"]))
            trim =''
            if 'trim' in vehicle_data_1[0]:
                trim = vehicle_data_1[0]['trim']
            basemsrp =0
            if 'baseMSRP' in vehicle_data_1[0]:
                basemsrp = vehicle_data_1[0]['baseMSRP']
            curb_weight =0
            if 'standardCurbWeight' in body_data:
                curb_weight = body_data['standardCurbWeight']
            # print(curb_weight)
            # print(basemsrp)
            estimatedMSRP =0
            if 'estimatedMSRP' in body_data:
                estimatedMSRP = body_data['estimatedMSRP']
            # engine_info =vehicle_data[0]['name']
            # print( (vehicle_data_2[0]))
            # print(vin,body_data['year'],body_data['make'],body_data['model'],'-',style_name,trim,engine_info,cylinder_info,fuel_info,curb_weight,country_of_origin,segment,transmission_type,transmission_type,drive_Type,basemsrp,estimatedMSRP,False)
            write_to_csv(vin,body_data['year'],body_data['make'],body_data['model'],'-',style_name,trim,engine_info,cylinder_info,fuel_info,curb_weight,country_of_origin,segment,transmission_type,transmission_type,drive_Type,basemsrp,estimatedMSRP,False)
            #     # if len(vin_data["Body"]) > 0:
            #     #     body_data = vin_data["Body"][0]
            #     #     bbdatafin = getBBData(vin,body_data['Model_Year'],body_data['Make'],body_data['Model'],body_data['Series_Name'])
            #     #     wholeacv = (bbdatafin[0])
            #     #     retailacv = (bbdatafin[1])

            #     #     write_to_csv(vin,body_data['Model_Year'],body_data['Make'],body_data['Model'],body_data['Salvage_Type'],body_data['Body_Style_Name'],body_data['Series_Name'],body_data['EngineInformation'],body_data['Cylinders'],body_data['Fuel_Type'],body_data['Base_Shipping_Weight'],body_data['CountryOfOrigin'],body_data['Segmentation_Description'],body_data['Transmission_Type_Description'],body_data['transmission_type'],body_data["Drive_Line_Type"],wholeacv,retailacv,False)
            #     # else:
            #     #     write_to_error_csv(vin,False)
           
            print(i)
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

def write_to_csv(vin="", modelyear="", makename="", modelname="", salvagetype="", bodystylename="", seriesname="", EngineInformation="", cylinders="", FuelTypeDescription="", BaseShippingWeight="", CountryOfOrigin="", SegmentationDescription="", TransmissionDescription="", TransmissionSpeed="",Drive_Line_Type="", BlackBookWACVValue ="",BlackBookRACVValue ="", Is_Header=True ):
        print(output_file_path)
        try:
            with open(output_file_path+".csv", mode='a',newline='') as csv_file:
                    fieldnames = ["vin","modelyear","makename","modelname","salvagetype","bodystylename","seriesname","EngineInformation","cylinders","FuelTypeDescription","BaseShippingWeight","CountryOfOrigin","SegmentationDescription","TransmissionDescription","TransmissionSpeed","Drive Line Type","BlackBook Whole ACV","BlackBook Retail ACV"]
                    
                    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                    if(not Is_Header):
                        csv_data= [vin , modelyear , makename , modelname , salvagetype , bodystylename , seriesname , EngineInformation , cylinders , FuelTypeDescription , BaseShippingWeight , CountryOfOrigin , SegmentationDescription , TransmissionDescription , TransmissionSpeed , Drive_Line_Type, BlackBookWACVValue,BlackBookRACVValue]
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
# post_vin_to_cvd('')