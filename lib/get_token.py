import requests
import json
import urllib3
import os
import os.path
import glob
from  requests.utils import quote
urllib3.disable_warnings()
env_vars = {}  
#f =open(os.path.join(os.path.split(os.path.dirname(__file__))[0], '.env'))
f =open(glob.glob('.env')[0],'r')
for line in f:
    if line.startswith('#') or not line.strip():
        continue
    key, value = line.strip().split('=', 1)
    env_vars[key]=value

def get_token():
    gettok = requests.post(env_vars["url"]+'/api/v1/token',
    headers = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*'}, verify=False,
    data = 'grant_type=password&username='+quote(env_vars['userapi'])+'&password='+quote(env_vars['passapi]'))
    if gettok.status_code == 200:
        tok=gettok.json()['access_token']
        return(True,tok)
    else:
        return(False,gettok.text)