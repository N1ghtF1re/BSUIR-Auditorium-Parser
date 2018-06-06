import requests

url = "https://students.bsuir.by/api/v1/auditory"

buildID = int(input('Введите номер корпуса: '))


response = requests.get(url)
kek = response.json()
for mem in kek:
	if mem['buildingNumber']['id'] == buildID:
		print(mem['name'], '-', mem['buildingNumber']['id'])
