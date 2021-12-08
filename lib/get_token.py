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
f =open(glob.glob('data/.env')[0],'r')

for line in f:
    if line.startswith('#') or not line.strip():continue
    key, value = line.strip().split('=', 1)
    env_vars[key]=value


def get_token():
    if not "apiuser" in env_vars or not "apipass" in env_vars:
        return(False,"not apipass or apiuser in .env")
    else:
        try:
            gettok = requests.post(env_vars["url"]+'/api/v1/token',
            headers = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*'}, verify=False,
            data = 'grant_type=password&username=' + quote(env_vars['apiuser']) + '&password=' + quote(env_vars['apipass']))
            return gettok.json()['access_token'] if gettok.status_code == 200 else False,gettok.text
        except requests.exceptions.RequestException as err:
            return "OOps:",err
            
