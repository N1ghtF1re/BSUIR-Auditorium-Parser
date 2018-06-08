import sqlite3
from getSchedule import getSchedule
from getAudiences import updateAudiencesTable
import datetime

def setLastUpdate(db_file): # Обновляем время обновление на текущее
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    time = datetime.datetime.now()
    strdate = time.strftime("%d.%m.%Y")

    cursor.execute("UPDATE config SET Value=:lastupdate WHERE Name='lastupdate'",{"lastupdate": strdate})
    conn.commit()

    conn.close()

def getLastUpdate(db_file): # Возвращаем дату последнего обновления
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM config WHERE Name='lastupdate'")
    results = cursor.fetchall()

    conn.close()

    return results[0][0]

def updateAllTables(db_file):
    print('Идет обновление базы данных... Это займет около 5 минут.')
    updateAudiencesTable(db_file)
    getSchedule(db_file)
    setLastUpdate(db_file)
    print('База данных обновлена!')
