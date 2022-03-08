import json
import holidays
import datetime

 

with open('/home/serena/Desktop/leanbit/ruby-challenge/level2/output.json', 'r') as f:
  data3 = json.load(f)
  

with open('/home/serena/Desktop/leanbit/ruby-challenge/level3/data.json', 'r') as f:
  data4 = json.load(f)
  

  

avail_dict = {}
avail_list = []



def week_days(since, until):
    #returns amount of week days in a certain date interval
    since_date = datetime.datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.datetime.strptime(until, "%Y-%m-%d").date()
    delta = (until_date - since_date).days
    counter = 0
    for i in range(delta + 1):
        day = since_date + datetime.timedelta(days=i)
        if day.weekday() in range(5):
            counter += 1
    return counter

def weekend_days(since, until):
    #returns amount of weekend days in a certain date interval
    since_date = datetime.datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.datetime.strptime(until, "%Y-%m-%d").date()
    delta = (until_date - since_date).days
    counter = 0
    for i in range(delta + 1):
        day = since_date + datetime.timedelta(days=i)
        if day.weekday() in [5,6]:
            counter += 1
    return counter


def holi_days(since, until):
    #returns amount of holidays in a certain date interval
    since_date = datetime.datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.datetime.strptime(until, "%Y-%m-%d").date()
    since_year = since_date.year
    until_year = until_date.year
    hol = holidays.CountryHoliday("IT", years=range(since_year, until_year+1)).keys()
    delta = (until_date - since_date).days
    counter = 0
    for i in range(delta + 1):
        day = since_date + datetime.timedelta(days=i)
        if day in hol and day.weekday() in range(5):
            counter += 1
    return counter


def is_feasible(effort_days, total_working_days):
    #estanlishes if effort days required are compatible with available working days
    if effort_days <= total_working_days:
        return True
    else:
        return False

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
        if datetime.date(years,day_month,day_day) >= since_date and datetime.date(years,day_month,day_day) <= until_date:
            if datetime.date(years,day_month,day_day).weekday() in range(5) and datetime.date(years,day_month,day_day) not in hol:
                counter+=1
    return counter


for i in range(len(data4["projects"])):
    period_dict = {}
    period_dict["period_id"] = data4["projects"][i]["id"]
    period_dict["total_days"] = (datetime.datetime.strptime(data4["projects"][i]["until"], "%Y-%m-%d").date()-datetime.datetime.strptime(data4["projects"][i]["since"], "%Y-%m-%d").date()).days + 1 
    period_dict["workdays"] = week_days(data4["projects"][i]["since"],data4["projects"][i]["until"])-holi_days(data4["projects"][i]["since"],data4["projects"][i]["until"]) - day_in_workdays(data4["projects"][i]["since"], data4["projects"][i]["until"], data4["local_holidays"][0]["day"])
    period_dict["weekend_days"] = weekend_days(data4["projects"][i]["since"],data4["projects"][i]["until"])
    period_dict["holidays"] = holi_days(data4["projects"][i]["since"],data4["projects"][i]["until"]) + day_in_workdays(data4["projects"][i]["since"], data4["projects"][i]["until"], data4["local_holidays"][0]["day"])
    total_working_days = 0
    #days are added to total_working_days if the project id is equal to the period id (for all the developers combined)
    for j in range(len(data3["availabilities"])):
        if data3["availabilities"][j]["period_id"] == data4["projects"][i]["id"]:
            total_working_days += data3["availabilities"][j]["workdays"]
    period_dict["feasibility"] = is_feasible(data4["projects"][i]["effort_days"], total_working_days)
    avail_list.append(period_dict)
    
    
avail_dict["availabilities"] = avail_list

    
with open('/home/serena/Desktop/leanbit/ruby-challenge/level3/output_serena.json', 'w') as f:
  json.dump(avail_dict, f, indent = 4)