

# list=[5,10,15,20,25,30,35,40,45,50,55,0,5,10,15,20]
# help_list=[]
# for i in range(len(list)):
#     if i !=len(list)-1:
#         if abs(list[i+1])>abs(list[i]):
#            help_list.append(abs(list[i+1])-abs(list[i]))
# st_list=[]
# for j in range(len(help_list)):
#     if j!=len(help_list)-1:
#         if help_list[j]==help_list[j+1]:
#             st_list.append(True)
#         else:
#             st_list.append(False)    
#     else:
#         if help_list[j]==help_list[j-1]:
#             st_list.append(True)
#         else:
#             st_list.append(False)          

# if all(st_list) and len(st_list)==len(help_list):
#     print(st_list)

import os
import sys
if len(sys.argv)>1:
    url=sys.argv[1]
    url=url.replace('https://','')
    if not url.endswith('/'):
        url+='/'
    # if url[-1]!="/":
    #     url+='/'
    print(url)
    if os.path.exists('..\password.txt'):
        print('exist')
    else:
        print('not exist')    
else:
    
    print('you have to enter url')


