

from fastapi import FastAPI,Request
from typing import Optional
from user import user_list
import threading
import time
from datetime import datetime
app=FastAPI()


def get_time_regular_attack(list):
    print('i am in get time regualr function')
    print(list)
    help_list=[]
    for i in range(len(list)):
        if i !=len(list)-1:
            if abs(list[i+1])>abs(list[i]):
                 help_list.append(abs(list[i+1])-abs(list[i]))
    st_list=[]
    for j in range(len(help_list)):
        if j!=len(help_list)-1:
            if help_list[j]==help_list[j+1]:
                st_list.append(True)
            else:
                st_list.append(False)    
        else:
            if help_list[j]==help_list[j-1]:
                st_list.append(True)
            else:
                st_list.append(False)          

    if all(st_list) :
        print(st_list)
        return True
    else:
        print(st_list)
        return False    

def get_time(time1,time2):
    time1=str(time1).split(':')
    time2=str(time2).split(':')
    if len(time1)==3 and len(time2)==3:
        min1=int(time1[1])
        sec1=int(time1[2])

        min2=int(time2[1])
        sec2=int(time2[2])
        if min1==min2:
            return  sec2-sec1
        else:
            seconds=0
            for m  in range(min1,min2):
                for s in range(sec1,60):
                    seconds+=1
                sec1=0
            seconds+=sec2
            return seconds



dic_ip={}

@app.get('/get-user')
def get_user(username: Optional[str]=None,password : str=None ,request : Request=None):
    client_host = request.client.host
    ttm=str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)
    

    if str(client_host) not in dic_ip.keys():
        dic_ip[str(client_host)]={'how_many':0,'start':'','end':'','st_block':False,'each_time':[]}
    else:

        if dic_ip[str(client_host)]['how_many']>=1000:
            return {'data':'limit'}
        
        if dic_ip[str(client_host)]['st_block']:
            return {'data':'blocked'}

        dic_ip[str(client_host)]['how_many']+=1   

        if len(dic_ip[str(client_host)]['each_time'])<=10:
             print('adding')
             dic_ip[str(client_host)]['each_time'].append(int(str(ttm).split(':')[2]))
        else:
            print('checking')
            st=get_time_regular_attack(dic_ip[str(client_host)]['each_time'])
            print(st)
            if dic_ip[str(client_host)]['how_many']>10 and st :
                print('regular attack handle')
                dic_ip[str(client_host)]['st_block']=True


        if dic_ip[str(client_host)]['how_many']==1:
            dic_ip[str(client_host)]['start']=ttm
        elif dic_ip[str(client_host)]['how_many']%5==0:
            dic_ip[str(client_host)]['end']=ttm
            # 12:30:12     ,    12:30:28
            get_sec=get_time(dic_ip[str(client_host)]['start'],dic_ip[str(client_host)]['end'])
            if get_sec<10:
                dic_ip[str(client_host)]['st_block']=True
            dic_ip[str(client_host)]['start']=ttm   

        
    print(dic_ip)

    for item_id in user_list:
        if user_list[item_id]['username']==username and user_list[item_id]['password']==password:
             return user_list[item_id]
    return {'data':'not found'}          
      



