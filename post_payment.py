import requests as rs
import time
import json
import os
import csv
# from dataaccess import read_from_csv,folder_input,init_csv

filename = 'input/payment_data.csv'


def readData():
   write_to_error_csv('',True)
    # List of ASAP data
   with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        i=0
        for row in datareader:
            
            # if(i>446772):
            # print(row[0], row[5], row[6],row[1],row[2])
            # post_payment(LoadId, PaymentAmount, PaymentTypeID,UserID,CreditCardOrderId)
            output = post_payment(row[0], row[5], row[6],row[1],row[2])
            # print(output['Status'])
            if output['Status'] == 'Error':
                # print('Error loadid = ',row[0],'Stock Number=',row[3])
                write_to_error_csv(row,False)
            i = i+1
            print(i) 
def write_to_error_csv(row,Is_Header=True ):
        # print(output_file_path)
        with open("output/post_payment_error.csv", mode='a',newline='') as csv_file:
                fieldnames = ["nload_id","created_userid","CreditCardOrderId","Stock_Number","towbill_number","payment_amount","payment_type_id"]
                
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,dialect='excel-tab')
                if(not Is_Header):
                    csv_data= row
                    # print(type(csv_data))
                    writer.writerow(csv_data)
                if(Is_Header):
                        writer.writerow(fieldnames)
def post_payment(LoadId, PaymentAmount, PaymentTypeID,UserID,CreditCardOrderId):
    try:
       
        # print()
        server = 'towapi' #'towapi' #'uat-iaatowwebapi' 
        # 'towapi'
        url = 'https://'+server+'.iaai.com' #base URL
        path = '/API/towapp/PostPaymenttoASAP' #post method for API
        headers ={'Content-Type':'application/json'}
        # values = {'ImportCount':80,'UserType':'IAATOW'} # IAATRANSPORTER Payload would vary for diffrent APIs
       
        # r = rs.post(url+path,headers=headers,data=json.dumps(values))
        r = rs.post(url+path,headers=headers,json={"LoadId": LoadId,
                                                    "PaymentList": [
                                                        {
                                                            "PaymentAmount": PaymentAmount,
                                                            "PaymentTypeID": PaymentTypeID
                                                        }
                                                    ],
                                                    "UserID": UserID,
                                                    "CreditCardOrderId": CreditCardOrderId
                                                })
        
        # print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

        

# post_payment(9049592, 735.00, 1,"2375","4509887442")
readData()