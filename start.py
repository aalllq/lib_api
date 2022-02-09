
import time
import arrow
import curses
from pick import pick,Picker
from modules import *
global err_arr
global ok_arr
global data_async
print(sys.platform)
##mk dirs##
#get_data("all_device")
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
    options = ['Fiscalize/Refiscalize','Get_device','beep'] + def_options
    menu(title,options)
    if options[index] == 'Fiscalize/Refiscalize' :
        title = "\nвыберите режим перефискализации"
        options = ['async_from file'] + def_options
        menu(title,options)
        if options[index] == 'async_from file' :
            print(fiscalizer("from_excel"))
    if options[index] == 'Get_device' :
            title =f"Выберите тип получения устройств"
            options = ['all_to_excel'] + def_options
            menu(title,options)
            if options[index] == 'all_to_excel' :
                data_writter("all_device","to_excel")
    
    if options[index] == 'beep' :
            title =f"Выберите источник данных"
            options = ['all_device','excel',"list"] + def_options
            menu(title,options)
            while True:
                start_time = time.time()
                beeper(options[index])
                print("--- %s seconds ---" % (time.time() - start_time))
    
                
            
except KeyboardInterrupt:
    print ('Interrupted')       


