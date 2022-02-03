import requests,json,urllib3
import os
import os.path
import glob
import random
import asyncio
from aiohttp import ClientSession
import sys
from  requests.utils import quote
#import xlrd
import excel2json
import openpyxl
import arrow
import time
import pandas as pd
import numpy as np
import xlsxwriter
from tkinter import filedialog as fd
import logging
urllib3.disable_warnings()

####first run#### do not put code before make_dir(),and get_token()

#f =open(os.path.join(os.path.split(os.path.dirname(__file__))[0], '.env'))

#принимает список папок, создает если их нет
def make_dir(paths):
    for path in paths:
        isExist = os.path.exists(path)
        if not isExist:
            try:
                os.makedirs(path)  
                print(f"{glob.glob(path)} папка создана в директории запуска программы ")
                time.sleep(2)
            except:
                print(f" не удалось создать папки{paths}")
paths= ["log","output"]
make_dir(paths)



start_time=arrow.now().format("YY-MM-DD_HH")
logging.basicConfig(filename=(f'log/{start_time}.log'), 
                    format='[%(asctime)s] [%(levelname)s] => %(message)s', 
                    level=logging.DEBUG)
logging.info('programm_started')  
                
def get_token():
    try:
        f =open(glob.glob('.env')[0],'r')
        env_vars = {} 
    except Exception as e:
        print(f"Нет Файла .env {e}")
        logging.error(f"Нет Файла .env {e}")
    for line in f:
        if line.startswith('#') or not line.strip():continue
        key, value = line.strip().split('=', 1)
        env_vars[key]=value
    if not "apiuser" in env_vars or not "apipass" in env_vars:
        return(False,"not apipass or apiuser in .env")
    else:
        env_url=env_vars["url"]
       # try:
        urls=[env_url +'/api/v1/token']
        header = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded','Accept': 'application/json, text/plain, */*'}
        data = 'grant_type=password&username=' + quote(env_vars['apiuser']) + '&password=' + quote(env_vars['apipass'])
        sender_action="get_token"
        method="POST"
        
       # print(sender_action,urls,headers,data,method)
        async_send(urls,method,sender_action,data=data,header=header) 
        print(tok)
       # tok= gettok.json()["access_token"]
        #logging.info(f"get token={tok}")  
        return env_vars,env_url    
                     
   #     except:
        #return "NOT get auth  token:"
#try:
#global  tok,env_vars,env_url
#tok,env_vars,env_url =get_token()
#print("globals",tok,env_vars,env_url)
#except:
#logging.error("not get globals check env")
#print("not get globals")
#exit()
### получение токена пароль  из  .env в корневой директории, retunr global env_url, global env_vars_dicts #####################################################        
"""
def get_token():
    try:
        f =open(glob.glob('.env')[0],'r')
        env_vars = {} 
    except:
        print("Нет Файла .env")
        logging.error("Нет Файла .env")
    for line in f:
        if line.startswith('#') or not line.strip():continue
        key, value = line.strip().split('=', 1)
        env_vars[key]=value
    if not "apiuser" in env_vars or not "apipass" in env_vars:
        return(False,"not apipass or apiuser in .env")
    else:
        env_url=env_vars["url"]
        try:
            get_tok_url=env_url+'/api/v1/token'
            gettok = requests.post(get_tok_url,
            headers = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*'}, verify=False,
            data = 'grant_type=password&username=' + quote(env_vars['apiuser']) + '&password=' + quote(env_vars['apipass']))
            if gettok.status_code == 200:
                tok= gettok.json()["access_token"]
                logging.info(f"get token={tok}")  
                return tok,env_vars,env_url
                     
            else:
                error = "not 200 status get token check url in env, current url=" + get_tok_url
                logging.info(error)  
                return   error
        except requests.exceptions.RequestException as err:
            return "NOT get auth  token:",err
try:
    global  tok,env_vars,env_url
    tok,env_vars,env_url =get_token()
    print("globals",tok,env_vars,env_url)
except:
    logging.error("not get globals check env")
    print("not get globals")
    exit()
"""
    
################################################################################################################################################################







    
    

#Задаем вопрос если N выходим
def yes_no():
    quest=input(f"press KEY \n\n Y-OK \n N= exit\n")
    if quest == "N"  or quest == "n":
        exit("EXIT")
        
def get_file():
    try:
        filename = fd.askopenfilename()
        return filename
    except:
        logging.error("error get filepath in module get_file()")

####### get action return json
def get_device(action):
    if action == "all":
        get_device_url = env_url + '/api/v1/devices?count=100000'
    else:
        logging.error("not valid action in get_device")
        print("not valid action in get_device")
    try:
        response = requests.get(get_device_url,headers= {'Authorization':'Bearer ' + tok, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
        status=response.status_code
        if response.status_code == 200:
            rj = response.json()
            status=response.status_code
            logging.info(f"get  device  in get_device, status:{status}")  
            return rj
        elif response.status_code != 200:
            logging.error(f"get  device  in get_device,{get_device_url}, status:{status}")

    except requests.exceptions.RequestException as err:
        logging.error(err,'error get devices in get_devices',url) 
 
 
  
#### get format return obj  format = "exel","sn_list",
def file_parser(format,file):
    try:
        if format == "excel":
            excel = pd.read_excel(file, engine='openpyxl',dtype=str)
            parser_out = excel.to_json()
            parser_out =json.loads(parser_out)
            return parser_out    
        else:
            logging.error(f"error not format {format} in module parser()")   
    except:
            logging.error(f"error parse {file} in module parser()")
    



##### dvalidate types lens types=sn =(validate=sn,fn,rnm)
def validator(obj,action):
    try:
    #    print(type(obj))
        if action == "sn":
            if  obj == None:
                return False
            if len(obj) != 16:
                return False 

            else:
                return True            
    except:
        logging.error(f"error validate {obj} in module validator()")


def fiscalizer(action):
    if action == "from_excel":
        logging.info(f" start modelu fiscalization {action}")
        print("выберите файл JSON для фискалзиации")
        file=get_file()
        all_device =get_device("all")
        file_json=_file_parser(excel,file)
        print(file_json)
    if action == "from_excel":
        print("list")
    
    
    
###### sender#### 
err_arr=[]
ok_arr=[]

async def fetch(url, session,method,sender_action,**kwargs):
    
    async with session.request(method,url,data=kwargs["data"],headers=kwargs["header"]) as response:
        print(response.status)
        if response.status == 200:
            ok_arr.append(response.status)
            #time.sleep(5)
        if sender_action== "get_token":
            global tok
            tok = await response.json()
            
            
              
        else:
            err_arr.append(reponse.status)
             
#        print(f"ok={ok} err={err}")
            
          # print(response.text)
   # return  ok_arr,err_arr

async def bound_fetch(sem, url, session,method,sender_action,**kwargs):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session,method,sender_action,**kwargs)
 #   return ok_arr,err_arr
        
async def run(urls,method,sender_action,**kwargs):
    tasks = []    
    sem = asyncio.Semaphore(160)
    async with ClientSession() as session:
      #  print(len(urls))
        if len(urls) == 1:
            url=urls[0]
        #for url in range(len(urls)):
         #   print(url,urls)
            task = asyncio.ensure_future(bound_fetch(sem, url.format(url),session,method,sender_action,**kwargs))
            tasks.append(task)
            
        responses = asyncio.gather(*tasks)
        await responses
     #   return ok_arr,err_arr

def async_send(urls,method,sender_action,**kwargs):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls,method,sender_action,**kwargs))
    loop.run_until_complete(future)
    #print(urls,method,sender_action)
    print("error=",len(err_arr),"OK=",len(ok_arr))
    ok_arr.clear()
    err_arr.clear()
    return ok_arr,err_arr



