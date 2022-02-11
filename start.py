
from csv import excel
import time
import arrow
import curses
from pick import pick,Picker
from modules import *

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
    title = f"Выберите дейтсвие"
    options = ['Fiscalize/Refiscalize','get_info','beep'] + def_options
    menu(title,options)
    if options[index] == 'Fiscalize/Refiscalize' :
        title = "\nвыберите режим перефискализации"
        options = ['async_from file'] + def_options
        menu(title,options)
        if options[index] == 'async_from file' :
            print(fiscalizer("from_excel"))
    if options[index] == 'get_info' :
            title = f"Выберите тип получения устройств"
            options = ['all_device',"all_groups","all_orgs"] + def_options
            menu(title,options)
           # if options[index] == 'all_to_excel' :
            data_writter(options[index],"to_excel")
    
    if options[index] == 'beep' :
            title = f"Выберите источник данных"
            options = ['all_device','excel',"sn_list","for_comment"] + def_options
            menu(title,options)
            beeper(options[index])
                
            
except KeyboardInterrupt:
    print ('Interrupted')       


