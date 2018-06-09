import sqlite3
from getSchedule import getSchedule
from getAudiences import updateAudiencesTable
import datetime



def setLastUpdate(cursor, conn): # Обновляем время обновление на текущее
    time = datetime.datetime.now()
    strdate = time.strftime("%d.%m.%Y")

    cursor.execute("UPDATE config SET Value=:lastupdate WHERE Name='lastupdate'",{"lastupdate": strdate})
    conn.commit()

def getLastUpdate(cursor): # Возвращаем дату последнего обновления

    cursor.execute("SELECT value FROM config WHERE Name='lastupdate'")
    results = cursor.fetchone()

    return results[0]

def updateAllTables(cursor, conn): # Обновляем все таблицы базы данных
    print('Идет обновление базы данных... Это займет около 5 минут.')
    updateAudiencesTable(cursor, conn)
    getSchedule(cursor, conn)
    setLastUpdate(cursor, conn)
    print('База данных обновлена!')
