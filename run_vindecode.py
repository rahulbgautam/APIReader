import requests as rs
import time

def post_file(start_index,imageIndex):
    try:
        #'http://localhost:54111/ImageUpload/AddVehicleMedia'
        vin = 'JH4CL968X8C019721' #'JAFSR175LDM465808'
        server = 'pevmweb0'+str(imageIndex)
        url = 'http://'+server+'.iaai.com' #base URL
        path = '/api/iaadecodevin' #get method for API
        headers ={'ApplicationId':'Guest','AuthenticationKey':'GuestPwd'}
        file_name = 'test.png' #File name should be in the same folder where u run the script from
        # upload_index = start_index
        values = {'vin':vin} #Payload would vary for diffrent APIs
        # multiple_files = [('file', (file_name, open(file_name, 'rb'), 'image/png'))]
        # r = rs.post(url+path, data=values,files=multiple_files)
        print(url+path)
        r = rs.get(url+path,headers=headers,params=values)
        print(r.content) #display the reponse from Api call 
    except Exception as error:
        print(error)
 
n=4 #Count for how many time you want to call the end-point
i=1
j=0 
st_salvage_id = 26708171 #26313315 #22213820
cont = True
#26313315
#26708171 #Dummy starting SalvageId 
while j <20000:
    while i<=n:
        print(i)
        post_file(0,i) #Calls the method to upload files 
        time.sleep(0.25)
        # print(st_salvage_id)
        # print(i)
        i =i+1
    j=j+1
    i=1
    print('j',j)
    