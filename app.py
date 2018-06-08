import requests
from getEmployedFromDB import getEmployedAud
#from getAudiences import updateAudiencesTable
from getAudiences import getAudiencesList

db_file = 'db\schedule.sqlite' # Файл базы данных SQLLite

buildID = int(input('Введите номер корпуса: '))
Floor = int(input('Введите этаж(-1, если не имеет значение): '))

#updateAudiencesTable(db_file)


allAuds = getAudiencesList(Floor, buildID, db_file)
employed = getEmployedAud(db_file); # Получаем множество занятых аудиторий

freeAud = allAuds - employed # Исключаем из множества всех аудиторий множество занятых аудиторий

print('Свободные аудитории: ')

for aud in freeAud:
	print(aud)

if freeAud == set():
	print('Нет свободных аудиторий ;c')
