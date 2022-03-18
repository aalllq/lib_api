
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
    options = ['get_info',"device_actions","fiscalization"] + def_options
    menu(title,options)
    if options[index] == 'get_info' :
            title = f"Выберите что хотите получить запиcь excell"
            options = ["all_device","all_groups","all_orgs"] + def_options
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
    if options[index] == 'fiscalization' :
        title = "\n Выберите действие\n"
        options = ['fiscalize','save_rnm','-close_fn','-validate_kkt'] + def_options
        menu(title,options)
        action = options[index]
        title = f"\n выбрано действие {action} --- выберите источник устройство \n"
        options = ['excel'] + def_options
        menu(title,options)
        yes_no(f"selected {action}, источник {options[index]} ?")
        fiscalizer3000(action,options[index])
                
    
except KeyboardInterrupt:
    print ('Interrupted')       


