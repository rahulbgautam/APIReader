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
            meta_data = vin_data["results_meta"]
            score_data = vin_data["results_score"]
            for result in range(0,int(meta_data["page_count"])):
                main_data = vin_data["results"][result]
                location_data = vin_data["results"][result]["location"]
                image_data = vin_data["results"][result]["images"]
                pricing_data = vin_data["results"][result]["pricing"]
                owner_data = vin_data["results"][result]["owner"]
                review_data=vin_data["results"][result]["reviews"]
                purchase_data=vin_data["results"][result]["purchase_information"]
                partner_data= vin_data["results"][result]["partner_info"]
                # all seeprate files need main_data['id'] as an identifier
                # vin_data["results"][0]["owner"]
                # 
                # vin_data["results"][0]["partner_info"]
                # vin_data["results"][0]["partner_info"]["partner_location"]
                print(vin,',',main_data['id'])
                #Top level data

               

                desc = ""
                if main_data['description']:
                        desc = main_data['description'].encode("utf-8", "ignore") 
            
                nicknm = ""
                if main_data['nickname']:
                    nicknm = main_data['nickname'].encode("utf-8", "ignore")
        
                purchase_price_currency =""
                if purchase_data['purchase_price_cents']:
                    purchase_price_currency=purchase_data['purchase_price_cents']


                multi_day_cta = ""
                if pricing_data['multi_day_cta'] :
                    multi_day_cta = pricing_data['multi_day_cta'].encode("utf-8", "ignore") 

                title = ""
                if main_data['title']:
                    title = main_data['title'].encode("utf-8", "ignore") 
                
                category =""
                if main_data['category']:
                    category = main_data['category'].encode("utf-8", "ignore") 



                write_to_main_csv(main_data['id'],main_data['pretty_id'],main_data['uuid'],score_data[result]['distance'],score_data[result]['distance_unit'],review_data['ratings_average'],review_data['ratings_count'],pricing_data['multi_day_discounts'],main_data['state'],location_data['city'],location_data['region'],location_data['region_abbreviation'],location_data['country'],location_data['country_abbreviation'],location_data['search_latitude'],location_data['search_longitude'],location_data['search_radius_meters'],main_data['make'],main_data['model'],main_data['year'],main_data['same_day_rentable'],desc,nicknm,category,main_data['timezone'],main_data['listed_at'],main_data['trips_taken_count'],title,main_data['motorcycle_show_page'],main_data['daily_rental_price_cents'],main_data['daily_rental_price_currency'],pricing_data['lowest_daily_rental_price']['lowest_daily_rental_price_cents'],main_data['displacement_cc'],main_data['featured'],main_data['fuel_capacity_gal'],main_data['is_partner'],main_data['created_at'],main_data['updated_at'],multi_day_cta,purchase_data['purchasable'],purchase_data['purchase_price_cents'],purchase_price_currency,purchase_data['high_value'],False)
                
                if main_data['is_partner'] == True:
                    write_to_partner_csv(main_data['id'],partner_data['partner_type'],partner_data['partner_name'],partner_data['partner_parent_company'],partner_data['partner_inventory_count'],partner_data['partner_banner'],False)




                #Image dataI
                
                for img in range(0,len(image_data)):
                    image_type = ""
                    if image_data[img]['id']:
                        image_type = image_data[img]['id']

                    image_name = ""
                    if image_data[img]['name']:
                        image_name = image_data[img]['name']

                    image_desc = ""
                    if image_data[img]['description']:
                        image_desc = image_data[img]['description']
                  
                  
                    write_to_image_csv(main_data['id'],image_data[img]['id'],image_data[img]['thumbnail_url'],image_data[img]['url'],image_data[img]['jpg_url'],image_data[img]['position'],image_data[img]['uuid'],image_data[img]['cloudinary_public_id'],image_type,image_name,image_desc,False)

                #Pricing data
                
                for prc in range(0,len(pricing_data['multi_day_pricing'])):
                    
                    disc_days = pricing_data['multi_day_pricing'][prc]['discount_days']
                    disc_per = pricing_data['multi_day_pricing'][prc]['discount_percent']
                    # print(disc_days)
                    if disc_days:
                        write_to_pricing_csv(main_data['id'],disc_days,disc_per,False)

                # Pricing data
                
                write_to_owner_csv(main_data['id'],owner_data['id'],owner_data['pretty_id'],owner_data['uuid'],owner_data['user_id'],owner_data['state'],owner_data['first_name'],owner_data['last_name_initial'],False)

               
            i=i+1
    except Exception as error:
        print(error)
        pass
    
       

def write_to_main_csv(data_id="",pretty_id="",uuid="",distance="",distance_unit="",ratings_average="",ratings_count="",multi_day_discounts="",state="",city="",region="",region_abbreviation="",country="",country_abbreviation="",search_latitude="",search_longitude="",search_radius_meters="",make="",model="",year="",same_day_rentable="",description="",nickname="",category="",timezone="",listed_at="",trips_taken_count="",title="",motorcycle_show_page="",daily_rental_price_cents="",daily_rental_price_currency="",lowest_daily_rental_price="",displacement_cc="",featured="",fuel_capacity_gal="",is_partner="",created_at="",updated_at="",multi_day_cta="",purchasable="",purchase_price_cents="",purchase_price_currency="",high_value="",Is_Header=True ):
        # print(output_file_path)
        try:
            
            with open(main_file_path+'.csv', mode='a') as csv_file:
                    fieldnames = ["id","pretty_id","uuid","distance","distance_unit","ratings_average","ratings_count","multi_day_discounts","state","city","region","region_abbreviation","country","country_abbreviation","search_latitude","search_longitude","search_radius_meterssearch_radius_meters","make","model","year","same_day_rentable","description","nickname","category","timezone","listed_at","trips_taken_count","title","motorcycle_show_page","daily_rental_price_cents","daily_rental_price_currency","lowest_daily_rental_pricelowest_daily_rental_price","displacement_cc","featured","fuel_capacity_gal","is_partner","created_at","updated_at","multi_day_cta","purchasable","purchase_price_cents","purchase_price_currency","high_value"]
                    writer = csv.writer(csv_file, delimiter=',')
                    if(not Is_Header):
                        csv_data= [data_id,pretty_id,uuid,distance,distance_unit,ratings_average,ratings_count,multi_day_discounts,state,city,region,region_abbreviation,country,country_abbreviation,search_latitude,search_longitude,search_radius_meters,make,model,year,same_day_rentable,description,nickname,category,timezone,listed_at,trips_taken_count,title,motorcycle_show_page,daily_rental_price_cents,daily_rental_price_currency,lowest_daily_rental_price,displacement_cc,featured,fuel_capacity_gal,is_partner,created_at,updated_at,multi_day_cta,purchasable,purchase_price_cents,purchase_price_currency,high_value]
                        # print(type(csv_data))
                        writer.writerow(csv_data)
                    if(Is_Header):
                            writer.writerow(fieldnames)
        except Exception as err:
            print(err)
            pass
        
                
def write_to_image_csv(data_id="",image_id="",thumbnail_url="",url="",jpg_url="",position="",uuid="",cloudinary_public_id="",image_type="",image_name="",image_desc="",Is_Header=True ):
        try:       # print(output_file_path)
            with open(image_file_path+'.csv', mode='a') as csv_file:
                fieldnames = ["data_id","image_id","thumbnail_url","url","jpg_url","position","uuid","cloudinary_public_id","image_type","image_name","image_desc"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= [data_id,image_id,thumbnail_url,url,jpg_url,position,uuid,cloudinary_public_id,image_type,image_name,image_desc]
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