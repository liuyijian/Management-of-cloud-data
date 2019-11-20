import requests

url= 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=QjYMAcsrNnyii5rwlZUhvHrT&client_secret=twTS8gu1fCNQ8GXZDAGYmeoOGMfYhMFE'
res = requests.get(url)
print(res.json()['access_token'])