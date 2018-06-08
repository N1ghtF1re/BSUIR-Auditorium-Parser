# Модуль содержит процедуру, возвращающую множество занятых аудиторий

import sqlite3
import requests
import json
import datetime

def getAudList(str):
    str = str.replace("'", '');
    str = str.replace("[", '')
    str = str.replace("]", '')
    str = str.replace(" ", '')
    str = str.replace("a", 'а')
    return str.split(',')

def getEmployedAud():
    url = 'http://students.bsuir.by/api/v1/week'

    response = requests.get(url)
    week = response.json() # Текущая неделя

    # Подключаемся к БД
    conn = sqlite3.connect('db\schedule.sqlite') # Название файлика с БД

    cursor = conn.cursor() #

    employed = set(); # Множество занятых аудиторий

    currWeekDay = datetime.datetime.today().weekday(); # Номер текущей недели (0 - понедельник)
    nowTime= datetime.datetime.now() # Текущее время.
    nowTime = 60*(nowTime.hour) + nowTime.minute # Формат времени - количество минут начиная с 00:00
    cursor.execute("SELECT * FROM Schedule WHERE StartTime < :nt AND EndTime > :nt AND Day = :d", {'nt': nowTime, 'd': currWeekDay})
    results = cursor.fetchall()

    for row in results:
        lessonWeeks = json.loads(row[4])
        if week in lessonWeeks: # На этой недели занятие есть
            audStrList = row[2]
            audList = getAudList(audStrList)
            for aud in audList:
                employed.add(aud) # Добавляем аудиторию в множество
    return employed
