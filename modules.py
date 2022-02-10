import requests,json,urllib3
import os

import os.path
import glob
import random
import asyncio
import aiohttp
from aiohttp import ClientSession,ClientTimeout,TCPConnector
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
                print(f"{glob.glob(path)} папка создана в директории запуска программы  ПЕРЕЗАПУСТИТЕ ПРИЛОЖЕНИЕ")
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
            async_send(urls,method,sender_action,data=data,header=header)
            if ok_arr[0] == 200:
                tok=data_async[0]['access_token']
                logging.info(f'get token ok={tok}')
                return tok,env_vars,env_url
            else:
                logging.error(f"not get token ok_code:data:err_code={ok_arr[0]}")
        except Exception as e:
            print(f"NOT get auth  token: {e}")
            logging.error(f"NOT get auth  token: {e}")


#Задаем вопрос если N выходим
def yes_no(*args):
    quest=input(f"\n\n\npress KEY \n\n Y-OK \n N= exit\n\n{args} \n\n")
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
        async_send(url,method,action, header= {'Authorization':'Bearer ' + tok, 'Content-type':'application/json', 'Accept': 'application/json'},data=data)
        if ok_arr[0] == 200:
            data=data_async
            logging.info(f"get  device  in get_data,ok status:{len(ok_arr)}")
            return data
            
        else:
            logging.error(f"get  device  in get_data error status {err_arr}")

    except requests.exceptions.RequestException as err:
        logging.error(err,'error get data in get_datas',url)



#### get format,file return obj  format = "exel","sn_list",
def file_parser(format):
    file=get_file()
    try:
        if format not in ['excel','sn_list']:logging.error(f"error not format {format} in module parser()")
        elif format == "excel":
            excel = pd.read_excel(file, engine='openpyxl',dtype=str)
            parser_out = excel.to_json()
            parser_out = json.loads(parser_out)
        elif format == "sn_list":
            parser_out=[]
            f =open(file)
            for line in f:
                if line.startswith('#'):continue #or not line.strip()
                parser_out.append(line.strip().split(';'))
            #print(pd.DataFrame.to_json(pd.DataFrame(parser_out)))
        return parser_out
 
    except Exception as e:
            logging.error(f"error parse {file} in module parser()  {e}")




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
        #print(response.status,arrow.now())
        if  sender_action in ["get_token","all_device"] :
            if response.status == 200:
                ok_arr.append(response.status)
                data_async.append(await response.json())
            else:
                err_arr.append(response.status)
        if sender_action in ["beep"]:
            if response.status !=200:
                err_arr.append(url)
            elif response.status == 200:
                ok_arr.append(url)
            

async def bound_fetch(sem, url, session,method,sender_action,**kwargs):
    async with sem:
       await fetch(url, session,method,sender_action,**kwargs)


async def run(urls,method,sender_action,**kwargs):
    tasks = []
    sem = asyncio.Semaphore(165)
    conn = TCPConnector(limit=50)
    #timeout = ClientTimeout(total=15)
    async with ClientSession(connector=conn) as session:
        if len(urls) == 1:
            url=urls[0]
            task = asyncio.ensure_future(bound_fetch(sem, url.format(url),session,method,sender_action,**kwargs))
            tasks.append(task)
        elif len(urls) > 1:
            for url in urls:

                task = asyncio.ensure_future(bound_fetch(sem, url.format(url),session,method,sender_action,**kwargs))
                tasks.append(task)
        await asyncio.gather(*tasks)


def async_send(urls,method,sender_action,**kwargs):
    global err_arr
    global ok_arr
    global data_async
    err_arr=[]
    ok_arr=[]
    data_async=[]
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls,method,sender_action,**kwargs))
    loop.run_until_complete(future)
        

    ########################################################################


###timer
def timer(times):
    for i in range(int(times),0,-1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(i)) 
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")
        #print(f"{int(i)}",  end="\r", flush=True)
        
     
def beeper(action):
    all_urls=[]
    urls=[]
    all_sn_list=[]
    comment_list=[]
    not_find_device=[]
    if action not in ["excel","all_device","sn_list","for_comment"]:
        logging.error(f'not valid action {action} in beeper')
    else:
        try:
            all_data=get_data("all_device")
            for kkt in all_data[0]:
                url = env_url +'/api/v1/devices/' + kkt['id']+'/beep'
                all_sn_list.append(kkt["serialNumber"])
                comment_list.append(kkt["comment"])
                all_urls.append(url)
            if action == "all_device":
                    urls=all_urls 
            if action == "sn_list":
                yes_no("Сейчас выдаст окно с выбора файла txt формат sn;any;any... либо sn  каждый с новой строки")
                kkt_list=file_parser(action)
                for sn in kkt_list:
                    if sn[0] in all_sn_list:
                        urls.append(all_urls[all_sn_list.index(sn[0])])
                    else: 
                        print(f"{sn[0]} kkt not find check sn\n")
                        
                   # print(all_urls[all_sn_list.index(sn[0])])
                   # print(all_sn_list[all_sn_list.index(sn[0])])

            
            for tic in range(5):
                print(f"\n\nwait send beep {len(urls)} device beep\n not find sn = {len(not_find_device)}\n\n")
                async_send(urls,"POST","beep", header= {'Authorization':'Bearer ' + tok, 'Content-type':'application/json', 'Accept': 'application/json'},data={})
                for i in urls:
                    if i in ok_arr:
                        print(f"ok_beep {all_sn_list[urls.index(i)]} {comment_list[urls.index(i)]}")
                for i in urls:
                    if i in err_arr:
                        print(f"err_beep {all_sn_list[urls.index(i)]} {comment_list[urls.index(i)]}")
                print(f"\n ok_beep={len(ok_arr)}\n err_beep={len(err_arr)}\n\n\n wait next beep 20sec")
                time.sleep(20)
            
        except Exception as e:
            print(f'error in beeper before while {e}')
     
            

### write data to_excel,to_list
def data_writter(data_type,action):
    if action not in ["to_excel","to_list"]:
        print(f"{action} not action in data_writter")
        logging.error(f"{action} not action in data_writter")
        time.sleep(5)
    elif action == "to_excel" and data_type == "all_device": 
        rj=get_data("all_device")
        aa=pd.json_normalize(rj[0])
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
