import requests
import sys
import updateDB
import sqlite3
import os
from getEmployedFromDB import getEmployedAud
from getAudiences import getAudiencesList

db_file = 'db\schedule.sqlite' # Файл базы данных SQLite

def writeFreeAud(cursor):
	while True:
		try:
			buildID = int(input('Введите номер корпуса: '))
			Floor = int(input('Введите этаж(-1, если не имеет значение): '))
		except ValueError:
			print('Вы вводите недопустимый символ -____-')
		else:
			break


	allAuds = getAudiencesList(cursor,Floor, buildID, db_file)
	employed = getEmployedAud(cursor); # Получаем множество занятых
	freeAud = allAuds - employed # Исключаем из множества всех аудиторий множество занятых аудиторий

	print('Свободные аудитории: ')

	for aud in freeAud:
		print(aud)

	if freeAud == set():
		print('Нет свободных аудиторий ;c')

try:
	# Подключаемся к БД
	conn = sqlite3.connect(db_file)
	cursor = conn.cursor()

	print('Добро пожаловать в приложение для поиска свободной аудитории')
	print('Последнее обновление: {0}. Чем чаще вы обновляетесь, тем точнее будет результат\n'.format(updateDB.getLastUpdate(cursor)))

	while True: # Пользовательское меню
		print('''Пожалуйста, выберите действие:
		1 - Поиск свободной аудитории
		2 - Выход из приложения
		9 - Обновление базы данных
		''')
		while True:
			try:
				answer = int(input('>> '))
				if answer in {1,2,9}:
					break
			except ValueError:
				print('Хватит вводить недопустимые символы!')

		if answer == 1:
			writeFreeAud(cursor)
			break
		elif answer == 9:
			updateDB.updateAllTables(cursor, conn)
		else:
			exit(0)
except sqlite3.Error as e:
	print('\nВозникла ошибка при работе с БД. Ошибка: ', e.args[0])
	print('Возможно файл БД отсуствует или открыт в другом приложении.')
finally:
	conn.close()

if os.name == 'nt':
	input('\nНажмите ENTER для выхода из приложения') # Ожидание ввода, чтобы приложение не закрывалось сразу при открытии через ярлык в windows
