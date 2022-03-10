import pandas as pd 


device = [{"sn":"123456","inn":"718837","state":{"blocked":False,"fn":"12354675"}},{"sn":"654321","inn":"77777","state":{"blocked":"False","fn":"654321"}}]
rnm_dict= {"rnm":"134590442","date":"2020"  }
#for d in device:
    #print(d)
a=pd.concat([pd.DataFrame(l)for l in device],axis=1)
print(a)