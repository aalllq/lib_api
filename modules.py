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


### получение токена пароль  из  .env в корневой директории, retunr global env_url, global env_vars_dicts #####################################################

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
        logging.error("not apipass or apiuser in .env")
        return(False,"not apipass or apiuser in .env")

    else:
        try:
            env_url=env_vars["url"]
            urls=[env_url +'/api/v1/token']
            header = {'Authorization' : 'Basic Og==', 'Content-type':'application/x-www-form-urlencoded','Accept': 'application/json, text/plain, */*'}
            data = 'grant_type=password&username=' + quote(env_vars['apiuser']) + '&password=' + quote(env_vars['apipass'])
            sender_action="get_token"
            method="POST"
            vars=async_send(urls,method,sender_action,data=data,header=header)

            if vars[0][0][0] == 200:
                tok=vars[0][2]['data']['access_token']
                logging.info(f'get token ok={tok}')
                return tok,env_vars,env_url
            else:
                logging.error(f"not get token ok_code:data:err_code={vars}")
        except Exception as e:
            print(f"NOT get auth  token: {e}")
            logging.error(f"NOT get auth  token: {e}")


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
def get_data(action):
    method='GET'
    data=''
    if action == "all_device":
        url = [env_url + '/api/v1/devices?count=100000']
    else:
        logging.error("not valid action in get_data")
        print("not valid action in get_data")
    try:
        response = async_send(url,method,action, header= {'Authorization':'Bearer ' + tok, 'Content-type':'application/json', 'Accept': 'application/json'},data=data)
        if response[0][0][0] == 200:
            data=response[0][2]["data"]
            logging.info(f"get  device  in get_data, count ok status:{len(response[0][0])}")
            return data
            
        elif response.status_code != 200:
            logging.error(f"get  device  in get_data error status {response.status_code}")

    except requests.exceptions.RequestException as err:
        logging.error(err,'error get data in get_datas',url)



#### get format,file return obj  format = "exel","sn_list",
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




#####dvalidate types lens types=sn =(validate=sn,fn,rnm)
def validator(obj,action):
    try:
    #    print(type(obj))
        if action == "16":
            if  obj == None or len(obj) != 16:
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
        all_device =get_data("all")
        file_json=_file_parser(excel,file)
        print(file_json)
    if action == "from_excel":
        print("list")



###### sender####

async def fetch(url, session,method,sender_action,**kwargs):


    async with session.request(method,url,data=kwargs["data"],headers=kwargs["header"]) as response:
        if response.status == 200:
            ok_arr.append(response.status)
            if sender_action in ["get_token","all_device"]:
                data_async['data'] = await response.json()
            #   print(1,data_async)
        else:
            err_arr.append(reponse.status)
    return  ok_arr,err_arr,data_async


async def bound_fetch(sem, url, session,method,sender_action,**kwargs):
    # Getter function with semaphore.
    async with sem:
       a= await fetch(url, session,method,sender_action,**kwargs)
      
       return a

async def run(urls,method,sender_action,**kwargs):
    tasks = []
    sem = asyncio.Semaphore(160)
    async with ClientSession() as session:
        if len(urls) == 1:
            url=urls[0]
        #for url in range(len(urls)):
         #   print(url,urls)
            task = asyncio.ensure_future(bound_fetch(sem, url.format(url),session,method,sender_action,**kwargs))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        return await responses

      # return responses

def async_send(urls,method,sender_action,**kwargs):
    global err_arr
    global ok_arr
    global data_async
    err_arr=[]
    ok_arr=[]
    data_async={}
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(urls,method,sender_action,**kwargs))
        result=loop.run_until_complete(future)
      #  print(a)
        #print(urls,method,sender_action)
       # print(2,data_async)
       # print("error=",len(err_arr),"OK=",len(ok_arr))
        return result
    except:
        print(1)

    ########################################################################
#    while True:
       #     for i in range(20,0,-1):
      #          print(f"{i}", end="\r", flush=True)
     #           time.sleep(1)
     
def beeper(action,id_array):
    data=get_data("all_device")
    for kkt in data:
        print(kkt)


### write data to_excel,to_list
def data_writter(action):
    if action not in ["to_excel","to_list"]:
        print(f"{action} not action in data_writter")
        logging.error(f"{action} not action in data_writter")
        time.sleep(10)
    elif action == "to_excel": 
        rj=get_data("all_device")
        aa=pd.json_normalize(rj)
        df=pd.DataFrame(aa)
        filename='output/output_'+arrow.now().format('YYYY-MM-DD__HH_mm_ss')+'.xlsx'
#print(df['isContractTerminated'])
        try:
            df.to_excel(filename, sheet_name='Sheet_name_1',index=False,encoding='utf-8')
            print(f"{filename} written")
            logging.info(f"{filename} written")
        except:
            print(f"{filename} written")
            logging.info(f"{filename} not  written")


    


# this always last     
global  tok,env_vars,env_url
tok,env_vars,env_url =get_token()  
print(f"get login data {tok,env_vars,env_url}")
