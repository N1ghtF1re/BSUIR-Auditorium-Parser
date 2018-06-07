import requests
import datetime

def getEmployedAud():
    groupsURL = 'https://students.bsuir.by/api/v1/groups'

    response = requests.get(groupsURL)
    GroupList = response.json() #Список всех групп

    scheduleURL='https://students.bsuir.by/api/v1/studentGroup/schedule?studentGroup='

    nowTime= datetime.datetime.now()

    employed = set(); # Множество занятых аудиторий

    for group in GroupList:

        try:
            response = requests.get(scheduleURL+group['name'])
            schedule = response.json() # Полное расписание на сегодня для текущей группы (group)
            if schedule['todaySchedules'] != []:
                for lesson in schedule['todaySchedules']: # Перебор сегодняшних пар группы group
                    startTime = lesson['startLessonTime'].split(':'); #Начало лекции. 0 элемент - часы кортежа, 1 - минуты
                    endTime = lesson['endLessonTime'].split(':'); # Конец лекции
                    startTime = nowTime.replace(hour=int(startTime[0]), minute = int(startTime[1]))
                    endTime = nowTime.replace(hour=int(endTime[0]), minute = int(endTime[1]))
                    if startTime < nowTime < endTime: # Пара в данный момент идет
                        for aud in lesson['auditory']:
                            employed.add(aud);
        except KeyError: # API БГУИРа самый лучший ♥ (нет)
            'No schedule'
        except ValueError:
            'No schedule'
    print('Список аудиторий загружен...')
    return employed
