import requests

url = "https://students.bsuir.by/api/v1/auditory"

buildID = int(input('Введите номер корпуса: '))
Floor = int(input('Введите этаж( -1, если не имеет значение )'))

response = requests.get(url)
AudList = response.json()

for aud in AudList:
	currBuild = aud['buildingNumber']['id'] # Номер корпуса
	audID = aud['name']; # Номер аудитории
	if not(str(audID)[0] in {'1','2','3','4','5','6','7','8','9','0'}):
		continue
	currFloor = int(str(audID)[0]); # Этаж
	if (currBuild == buildID) and ((Floor == -1) or (currFloor == Floor)):
		print(audID, '-', aud['buildingNumber']['id'])
