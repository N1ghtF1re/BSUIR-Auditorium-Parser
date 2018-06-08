import requests
from getEmployedFromDB import getEmployedAud

url = "https://students.bsuir.by/api/v1/auditory"

buildID = int(input('Введите номер корпуса: '))
Floor = int(input('Введите этаж(-1, если не имеет значение): '))

response = requests.get(url)
AudList = response.json()

employed = getEmployedAud(); # Получаем множество занятых аудиторий

freeAud = set()

for aud in AudList:
	currBuild = aud['buildingNumber']['id'] # Номер корпуса
	audID = aud['name']; # Номер аудитории
	audID = audID.replace("a", 'а') # Странноее поведение буквы а, киррилистическая заменяется на латинскую
	if not(str(audID)[0] in {'1','2','3','4','5','6','7','8','9','0'}):
		continue
	currFloor = int(str(audID)[0]); # Этаж (Аудитории нумеруются так, что первая цифра - этаж)
	if (currBuild == buildID) and ((Floor == -1) or (currFloor == Floor)):
		currAud = str(audID) + '-' + str(aud['buildingNumber']['id'])
		currAud = currAud.replace(' ', '')
		if not (currAud in employed): # Проверяем, занята ли аудитория (В employed - множество занятых аудиторий)
			print(currAud)
			freeAud.add(currAud)

#print (employed)
if freeAud == set():
	print('Нет свободных аудиторий')
