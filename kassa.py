import requests
import json
import urllib3
import fileinput
#import argparse
#import pandas
#import arrow
urllib3.disable_warnings()
import os
import os.path
import glob
from lib.get_token import get_token


mode=(int(input('Выберите режим работы \n 1=Работа с файлом \n 2=Работа с БД \n, 3=Работа без API \n')))

print(get_token())
'''
if tok[0]== False:
    while True:
        f_mode=int((input("authFalse, press 1 = continue \n 2 = exit" +str(tok)))
        if f_mode != 1 or f_mode != 2
            print(env_vars)
        else:break'''

input('exit')