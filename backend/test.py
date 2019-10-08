import base64
from urllib import parse
import requests

with open('test.jpg', 'rb') as fin:
    image_data = fin.read()
    image_string = base64.b64encode(image_data)
    data = parse.urlencode({'image': image_string}).encode('utf-8')

response = requests.post(
    'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=24.ea04d58ba72c685e8238cf22de200bd2.2592000.1573126398.282335-16049065',
    data=data, 
    headers={'Content-Type':'application/x-www-form-urlencoded'}
)

body = response.json()

print(body)