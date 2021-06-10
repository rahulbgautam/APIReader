import requests as rs
import time
import json

def import_user():
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        # vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        print()
        server = 'qas-iaatowwebapi' 
        # 'towapi'
        url = 'https://'+server+'.iaai.com' #base URL
        path = '/API/towapp/ImportAuthUser' #get method for API
        headers ={'Content-Type':'application/json'}
        # file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = {'ImportCount':80,'UserType':'IAATRANSPORTER'} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        # print(url+path)
        r = rs.post(url+path,headers=headers,data=json.dumps(values))
        print(r.content) #display the reponse from Api call 
        return json.loads(r.content)
    except Exception as error:
        print(error)

def loop_import_user():
    count = 120000
    step =80
    start = 99963
    for i in range(start,count,step):
        import_user()
        print(i)
        

loop_import_user()