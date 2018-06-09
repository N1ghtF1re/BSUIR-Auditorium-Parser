# Получаем список аудиторий и закидываем его в БД.
# Таблтца базы данных состоит из 2 столбцов
# Столбец:    id  | Name            | Type                    | Building | Floor
# Описание:   -   | Номер аудитории | Тип аудитории(лк/пз/лр) | Корпус   | Этаж

import sqlite3
import requests

def updateAudiencesTable(cursor, conn):

    url = "https://students.bsuir.by/api/v1/auditory"

    response = requests.get(url)
    AudList = response.json()

    for aud in AudList:
        currBuild = aud['buildingNumber']['id'] # Номер корпуса
        audID = aud['name']; # Номер аудитории
        audType = aud['auditoryType']['abbrev']
        audID = audID.replace("a", 'а') # Странноее поведение буквы а, киррилистическая заменяется на латинскую
        if not(str(audID)[0] in {'1','2','3','4','5','6','7','8','9','0'}):
            continue
        currFloor = int(str(audID)[0]); # Этаж (Аудитории нумеруются так, что первая цифра - этаж)
        cursor.execute("insert into Audiences(Name, Type, Building, Floor)\
        values (:name, :type, :building, :floor)\
        ",{"name": audID, "type": audType, "building": currBuild, "floor": currFloor})
        conn.commit()

def getAudiencesList(cursor, floor, building, db_file):
    auds = set()

    if floor == -1:
        cursor.execute("SELECT * FROM Audiences WHERE building = :build", {'build': building})
    else:
        cursor.execute("SELECT * FROM Audiences WHERE Building = :build AND Floor = :floor", {'build': building, 'floor': floor})
    results = cursor.fetchall()

    for row in results:
        audID = row[1]
        audID = audID.replace("a", 'а') # Странноее поведение буквы а, киррилистическая заменяется на латинскую
        auds.add(audID+'-'+str(building))

    return auds
