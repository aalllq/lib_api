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


#mode=(int(input('Выберите режим работы \n 1=Работа с файлом \n 2=Работа с БД \n')))

print(get_token())
#print(env_vars)