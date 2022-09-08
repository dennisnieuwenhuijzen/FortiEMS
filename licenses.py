import requests
import json


# Suppress only the single warning from urllib3 needed.
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#Settings:
verifySSL = True
host = "emsserver.nl"
username='username'
password='password'

# login proces
url = f'https://{host}/api/v1/auth/signin'
data = { "name" : username, "password" : password }
headers = { "content-type" : "application/json" }

result = requests.post(url=url, json=data, headers=headers, verify=verifySSL)
authCookies = dict(result.cookies)

#Get total amount of Endpoints
offset = 0
count = 1
url = f'https://{host}/api/v1/endpoints/index'
headers = { "content-type" : "application/json" }
params = { "offset" : offset, "count" : count}
result = requests.get(url=url, headers=headers, params=params, cookies=authCookies, verify=verifySSL)
rDict = json.loads(result.__dict__["_content"].decode())
total = rDict["data"]["total"]
print("")
print(f"Found {total} records.")

def getEndpointData(offset, count):
    url = url = f'https://{host}/api/v1/endpoints/index'
    headers = { "content-type" : "application/json" }
    params = { "offset" : offset, "count" : count}
    result = requests.get(url=url, headers=headers, params=params, cookies=authCookies, verify=verifySSL)
    rDict = json.loads(result.__dict__["_content"].decode())
    return(rDict)

offset = 0
count = 50
c = 0
while offset < total:
    rDict = getEndpointData(offset, count)
    for endpoint in rDict["data"]["endpoints"]:
        if endpoint["is_ems_registered"]:
            c += 1
    offset += count
print(f'Registered (licensed) endpoints: {c}')
