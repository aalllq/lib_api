
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
    options = ['Fiscalize/Refiscalize','get_info','beep',"device_actions"] + def_options
    menu(title,options)
    if options[index] == 'Fiscalize/Refiscalize' :
        title = "\nвыберите режим перефискализации"
        options = ['async_from file'] + def_options
        menu(title,options)
        if options[index] == 'async_from file' :
            print(fiscalizer("from_excel"))
            
    if options[index] == 'get_info' :
            title = f"Выберите что хотите получить запиcь excell"
            options = ['all_device',"all_groups","all_orgs"] + def_options
            menu(title,options)
            data_writter(options[index],"to_excel")
            
    if options[index] == 'device_actions' :
        title = f"pick input device"
        options = ['all_device','excel',"sn_list","for_comment"]  + def_options
        menu(title,options)
        input_data=options[index]
        if input_data is not "Exit":
                title = f"pick action"
                options = ['reboot','beep']  + def_options
                menu(title,options)
                device_action(options[index],input_data)

except KeyboardInterrupt:
    print ('Interrupted')       


