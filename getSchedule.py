# Получаем расписание и закидываем его в БД.
# Таблтца базы данных состоит из 8 столбцов
# Столбец:    id  |  GroupName    |  Aud             | Day                      | StartTime      | EndTime             | StrTime
# Описание:   -   | Номер группы  | Список аудиторий | Номер дня недели(0 - пн) | Начало и конец ЛК в Hour*60 + Minute | Время лекции в строковом формате

import sqlite3
import requests
import json

daysnames = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def getSchedule(table):
    # Подключаемся к БД
    conn = sqlite3.connect(table)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Schedule')
    conn.commit()

    groupsURL = 'https://students.bsuir.by/api/v1/groups'

    response = requests.get(groupsURL)
    GroupList = response.json() #Список всех групп

    scheduleURL='https://students.bsuir.by/api/v1/studentGroup/schedule?studentGroup='

    for group in GroupList:
        try:
            response = requests.get(scheduleURL+group['name'])
            schedule = response.json() # Полное расписание на сегодня для текущей группы (group)
            if schedule['schedules'] != []:
                for day in schedule['schedules']: # Перебор сегодняшних пар группы group
                    days =  daysnames.index(day['weekDay'])
                    for lesson in day['schedule']:
                        weeks = str(lesson['weekNumber']) # Недели, по которым проходит пара
                        studentGroup = str(lesson['studentGroup'][0])
                        aud = str(lesson['auditory'])
                        times = str(lesson['lessonTime'])
                        startTime = lesson['startLessonTime'].split(':'); #Начало лекции. 0 элемент - часы кортежа, 1 - минуты
                        endTime = lesson['endLessonTime'].split(':'); # Конец лекции
                        startTime = 60 * int(startTime[0]) + int(startTime[1]) # Формат времени : кол-во минут, начиная с 00:00
                        endTime = 60 * int(endTime[0]) + int(endTime[1])


                        cursor.execute("insert into Schedule(GroupName, Aud, Day, Week, StartTime, EndTime, StrTime)\
                         values (:gn, :aud, :days, :week, :stime, :etime, :time)\
                          ",{"gn": studentGroup, "aud": aud,"days": days , "week":weeks, "stime" : startTime, "etime": endTime, "time":times})
                        conn.commit()


        except KeyError: # API БГУИРа самый лучший ♥ (нет)
            'No schedule'
        except ValueError:
            'No schedule'
    conn.close()
