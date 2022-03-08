import json
import holidays
import datetime


 
with open('/home/serena/Desktop/leanbit/ruby-challenge/level1/output.json', 'r') as f:
  data1 = json.load(f)
  
  
with open('/home/serena/Desktop/leanbit/ruby-challenge/level2/data.json', 'r') as f:
  data2 = json.load(f)
  
avail_dict = {}
avail_list = []


def day_in_workdays(since, until, day):
    #establishes if a day is a workday in a certain date interval
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    since_date = datetime.datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.datetime.strptime(until, "%Y-%m-%d").date()
    since_year = since_date.year
    until_year = until_date.year
    hol = holidays.CountryHoliday("IT", years=range(since_year, until_year+1)).keys()
    counter=0
    for years in range(since_year, until_year+1):
        day_month=day_date.month
        day_day=day_date.day
        #condition requires that the day is between "since" and "until" date and that it is neither a weekday nor a holiday
        if datetime.date(years,day_month,day_day) >= since_date and datetime.date(years,day_month,day_day) <= until_date:
            if datetime.date(years,day_month,day_day).weekday() in range(5) and datetime.date(years,day_month,day_day) not in hol:
                counter+=1
    return counter

def is_birthday_local_holiday(birthday, local_holiday):
    #establishes if the birthday is a local holiday
    birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
    local_holiday_date = datetime.datetime.strptime(local_holiday, "%Y-%m-%d").date()
    if birthday_date.month == local_holiday_date.month and birthday_date.day == local_holiday_date.day:
        return True
    


for j in range(len(data1["availabilities"])):
    for i in range(len(data2["developers"])):
        developer_dict = {}
        developer_dict["developer_id"] = data2["developers"][i]["id"]
        developer_dict["period_id"] = data1["availabilities"][j]["period_id"]
        developer_dict["total_days"] = data1["availabilities"][j]["total_days"]
        workdays = data1["availabilities"][j]["workdays"]
        holiday = data1["availabilities"][j]["holidays"]
        counter1 = day_in_workdays(data2["periods"][j]["since"], data2["periods"][j]["until"], data2["developers"][i]["birthday"])
        workdays-=counter1
        holiday+=counter1
        counter2 = day_in_workdays(data2["periods"][j]["since"], data2["periods"][j]["until"], data2["local_holidays"][0]["day"])
        if not is_birthday_local_holiday(data2["developers"][i]["birthday"], data2["local_holidays"][0]["day"]):
            workdays-=counter2
            holiday+=counter2
        developer_dict["workdays"] = workdays
        developer_dict["weekend_days"] = data1["availabilities"][j]["weekend_days"]
        developer_dict["holidays"] = holiday
        avail_list.append(developer_dict)
    
avail_dict["availabilities"] = avail_list        

    
with open('/home/serena/Desktop/leanbit/ruby-challenge/level2/output_serena.json', 'w') as f:
  json.dump(avail_dict, f, indent = 4)