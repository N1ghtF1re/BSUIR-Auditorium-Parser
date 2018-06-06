import requests
import numpy as np
import pandas as pd
import datetime

groupsURL = 'https://students.bsuir.by/api/v1/groups'

response = requests.get(groupsURL)
GroupList = response.json()

scheduleURL='https://students.bsuir.by/api/v1/studentGroup/schedule?studentGroup='
headers = {"Content-Type": "application/json"}

nowTime= datetime.datetime.now()

for group in GroupList:
    response = requests.get(scheduleURL+group['name'])
    schedule = response.json()
    
    for lesson in schedule['todaySchedules']:
        startTime = lesson['startLessonTime'].split(':'); #Начало лекции. 0 элемент - часы кортежа, 1 - минуты
        endTime = lesson['endLessonTime'].split(':'); # Конец лекции
        startTime = nowTime.replace(hour=int(startTime[0]), minute = int(startTime[1]))
        endTime = nowTime.replace(hour=int(endTime[0]), minute = int(endTime[1]))
        if startTime < nowTime < endTime:
            print(lesson['auditory'])
