import json
import requests
import urllib3
from lib.get_token import *
get_token()
import pandas as pd
import xlsxwriter

urllib3.disable_warnings()
i = 0



aa=pd.json_normalize(rj)
df=pd.DataFrame(aa)
filename='output/output_'+arrow.now().format('YYYY-MM-DD__HH_mm_ss')+'.xlsx'
#print(df['isContractTerminated'])
try:
   df.to_excel(filename, sheet_name='Sheet_name_1',index=False,encoding='utf-8')
except:
    print("lib.get_info.get_info()-Запись файла не удалась возможно нет папки output\n")



def get_ids(sn_array):
    response = requests.get(env_url+'/api/v1/devices?count=40',
    headers= {'Authorization':'Bearer ' + tok, 'Content-type':'application/json', 'Accept': 'application/json'}, verify=False)
    rj = response.json()
    id_array = []
    id_sn=[]
    for kkt in rj:
        if kkt['serialNumber'] in sn_array:
            id_array.append(kkt['id'])
            id_sn.append(kkt['serialNumber'])
    #print(id_array,id_sn)
    print()
    return id_array,id_sn

    


#pd.json_normalize(rj).to_csv(.1, encoding='utf-8', index=False)
                  
                  
'''print('SN','FN','ID','comment','GroupName','orgName','fiscalizedAt','networkAddress','macAddress','hasSdCard','error','closeTime','unsentDocumentsCount','fsDocumentsCount'
,'fsWarningFlags','fsExpirationDate','fsVersion','ofdName','ofdAddress','ofdPort','firmwareBuild',sep=';')
while  i < len(rj):
    print(rj[i]['serialNumber'], rj[i]["state"]["fsSerialNumber"], rj[i]['id'], rj[i]["comment"],rj[i]["deviceGroupName"],
    rj[i]["organizationName"],rj[i]["state"]["fiscalizedAt"],rj[i]["state"]["networkAddress"],rj[i]["state"]["macAddress"],
    rj[i]["hasSdCard"],rj[i]["state"]["error"]["message"],rj[i]["autoCloseShiftAt"],rj[i]["state"]["unsentDocumentsCount"],
    rj[i]["state"]["fsDocumentsCount"],rj[i]["state"]["fsWarningFlags"],rj[i]["state"]["fsExpirationDate"],rj[i]["state"]["fsVersion"],
    rj[i]["ofdName"],rj[i]["ofdAddress"],rj[i]["ofdPort"],rj[i]["state"]["firmwareBuild"],sep=';')
    id_array.append(rj[i]['id'])
    i = i + 1
#print(get_token.tok)

'''