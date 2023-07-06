# import the library module
import hashlib
import datetime
import random
import base64

def generateHash(): 
    # initialize a string
    str = "www.MyTecBits.com"
    
    # encode the string
    encoded_str = str.encode()
    
    # create a sha1 hash object initialized with the encoded string
    hash_obj = hashlib.sha1(encoded_str)
    
    # convert the hash object to a hexadecimal value
    hexa_value = hash_obj.hexdigest()
    
    # print
    print("\n", hexa_value, "\n")

def generateNonce():
    num = random.random()
    return num
def generateHashDigest(): 
    companyName = "Atmosphere"
    realm = "http://communitymanager"
    appId = "autodata-hEHbFOwyXMgsTghfmxXX8BEYPX28nLIklvcU74Tz"
    nonce = str(generateNonce())
    # ct stores current time
    ct = datetime.datetime.now()
    # ts store timestamp of current time
    timestamp = str(ct.timestamp()*1000)
    timestamp = timestamp[:13]
    sharedSecret = "c0a48eda7fa52a4756e99e6696a5f3b1e58fb95bde19de1309c4dd5472d8d0ef"
    digestMethod = "SHA1"
    companyPrefix = "chromedata_"
    secretDigestUnencrypted = nonce + timestamp + sharedSecret
    encoded_str = secretDigestUnencrypted.encode()
    # create a sha1 hash object initialized with the encoded string
    hash_obj = hashlib.sha1(encoded_str)
    # convert the hash object to a hexadecimal value
     
    message_bytes = hash_obj.digest()
    # .hexdigest()
    base64_bytes = base64.b64encode(message_bytes)
    secretDigest = base64_bytes.decode('ascii')   
    
    authorizationHeader = companyName + ' ' +'realm="' + realm + '", ' + companyPrefix + 'app_id="' + appId + '", ' + companyPrefix + 'nonce="' + nonce + '", ' + companyPrefix + 'secret_digest="' + secretDigest + '", ' + companyPrefix + 'version="1.0", ' + companyPrefix + 'digest_method="' + digestMethod + '", ' + companyPrefix + 'timestamp="' + timestamp + '"'
    # print(authorizationHeader)
    return authorizationHeader


generateHashDigest()
