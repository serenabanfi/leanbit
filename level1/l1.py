import json
import holidays
import datetime

with open('/home/serena/Desktop/leanbit/ruby-challenge/level1/data.json', 'r') as f:
  data = json.load(f)
  
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


for i in data["periods"]:
    period_dict = {}
    period_dict["period_id"] = i["id"]
    period_dict["total_days"] = (datetime.datetime.strptime(i["until"], "%Y-%m-%d").date()-datetime.datetime.strptime(i["since"], "%Y-%m-%d").date()).days + 1
    period_dict["workdays"] = week_days(i["since"],i["until"])-holi_days(i["since"],i["until"])
    period_dict["weekend_days"] = weekend_days(i["since"],i["until"])
    period_dict["holidays"] = holi_days(i["since"],i["until"])
    avail_list.append(period_dict)
    
    
avail_dict["availabilities"] = avail_list

with open('/home/serena/Desktop/leanbit/ruby-challenge/level1/output_serena.json', 'w') as f:
  json.dump(avail_dict, f, indent = 4)