import requests
from getEmployedFromDB import getEmployedAud
from getAudiences import getAudiencesList
import updateDB


db_file = 'db\schedule.sqlite' # Файл базы данных SQLLite

def writeFreeAud():
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

print('Добро пожаловать в приложение для поиска свободной аудитории')
print('Последнее обновление: {0}. Чем чаще вы обновляетесь, тем точнее будет результат'.format(updateDB.getLastUpdate(db_file)))
updateDB.setLastUpdate(db_file)
writeFreeAud()
