import requests

url = "https://students.bsuir.by/api/v1/auditory"

response = requests.get(url)
kek = response.json()
for mem in kek:
	print(mem['name'], '-', mem['buildingNumber']['id'])
