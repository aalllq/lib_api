import time
import arrow
import curses
from pick import pick,Picker
from modules import *

global  env_vars,env_url
env_vars,env_url =get_token()

##mk dirs##

def go_back(picker):
    return None, -1

def menu(title,options):
        picker = Picker(options, title)
        picker.register_custom_handler(curses.KEY_LEFT, go_back)
        global opion,index  
        option, index = picker.start()
        time.sleep(1)
      
try:
    def_options=['Exit']
    title =f"Выберите дейтсвие"
    options = ['Fiscalize/Refiscalize'] + def_options
    menu(title,options)
    if options[index] == 'Fiscalize/Refiscalize' :
        title = "\n\nвыберите режим перефискализации"
        options = ['async_from file'] + def_options
        menu(title,options)
        if options[index] == 'async_from file' :
            print(fiscalizer("from_excel"))
         
    
                
            
except KeyboardInterrupt:
    print ('Interrupted')       



