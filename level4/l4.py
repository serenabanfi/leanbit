import json
import datetime
import numpy as np


with open('/home/serena/Desktop/leanbit/ruby-challenge/level1/output.json', 'r') as f:
  data0 = json.load(f)
    
with open('/home/serena/Desktop/leanbit/ruby-challenge/level2/output.json', 'r') as f:
  data3 = json.load(f)
  
with open('/home/serena/Desktop/leanbit/ruby-challenge/level4/data.json', 'r') as f:
  data5 = json.load(f)
    


#string dates are converted to datetime.date
periods_since = []
periods_until = []

for i in range(len(data5["projects"])):
    periods_since.append(datetime.datetime.strptime(data5["projects"][i]["since"], "%Y-%m-%d").date())
    periods_until.append(datetime.datetime.strptime(data5["projects"][i]["until"], "%Y-%m-%d").date())


projects_days = [] #list containing effort days for each project
for i in range(len(data5["projects"])):
    projects_days.append(data5["projects"][i]["effort_days"])

tot_period_dev = np.zeros(len(data5["developers"]), dtype=int) #total of days that each developer can dedicate in the longest time period
#from now on, we are assuming that the first period includes the other two and they do not overlap: this works only for the specific case

array_period_dev = np.zeros((len(periods_since), len(data5["developers"])), dtype=int) #array containing the number of days that each developer can dedicate for each period

for i in range(len(data3["availabilities"])):
    a = data3["availabilities"][i]["period_id"]-1
    b = data3["availabilities"][i]["developer_id"]-1
    c = data3["availabilities"][i]["workdays"]
    array_period_dev[a][b] = c
    if a==0:
        tot_period_dev[b] = c

 
array_project_dev = np.zeros((len(periods_since), len(data5["developers"])), dtype=int) #array containing the number of days that each developer will dedicate to each project
#the idea is that we loop on the number of projects and assign days of work to each developer until:
#1) either the project is completed
#2) or the developer has no more working days available
#as a consequence, the first developer will have their schedule full, while the remaining may have some spare time to dedicate to other projects which are not listed here
    
for i in range(len(projects_days)):
    remain_days = projects_days[i] #how many days remain to conclude the project
    dev_num = 0 #developer id
    per_num = i #period id
    while dev_num < np.shape(array_project_dev)[1] and remain_days > 0:
        #the loop goes on until the developers run out or the project is completed
        period_dev = tot_period_dev[dev_num] #days that the developer can dedicate in this period of time
        day_num = array_period_dev[per_num,dev_num] #days that the developer can dedicate to this project
        day_num_min = min([remain_days, day_num, period_dev]) #days that the developer will dedicate
        array_project_dev[per_num,dev_num] += day_num_min #update of array_project_dev (dedicated days increase)
        array_period_dev[per_num,dev_num] -= day_num_min #update of array_period_dev (remaining days per period decrease)
        tot_period_dev[dev_num] -= day_num_min #the developer will now have fewer available days
        remain_days -= day_num_min #the project will now require fewer days to be concluded
        dev_num += 1 #next developer
        
        
        
#construction of final dictionary containing the project schedule for each developer and the remaining free days
final_dict = {}
avail_list = []
free_list = []

for j in range(np.shape(array_project_dev)[1]):                
    for i in range(np.shape(array_project_dev)[0]):
        project_dict = {}
        project_dict["project_id"] = i+1
        project_dict["developer_id"] = j+1
        project_dict["days_dedicated"] = int(array_project_dev[i][j])
        avail_list.append(project_dict)
    free_dict = {}
    free_dict["developer_id"] = j+1
    free_dict["free_days"] = int(tot_period_dev[j])
    free_list.append(free_dict)

final_dict["project_schedule"] = avail_list
final_dict["free_days_left"] = free_list

with open('/home/serena/Desktop/leanbit/ruby-challenge/level4/output_serena.json', 'w') as f:
  json.dump(final_dict, f, indent = 4)