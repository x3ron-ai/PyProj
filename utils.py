import json
import tabulate
import os
from exceptions import *
from tabulate import tabulate
from colorama import init as Colorama, Fore, Back
from msvcrt import getch as ReadKey
from time import sleep as Sleep
Colorama(autoreset=True)

Clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # Функция очищает окно консоли

class Menu:
	"""
	Объект меню для выбора
	"""
	def __init__(self, buttons: list):
		"""
		Конструктор класса, принимает массив с кнопками.

		:param buttons: - список кнопок
		"""
		self.buttons = buttons
		self.length = len(buttons)
		self.selected = 0
	def select(self):
		"""
		Запуск меню, возвращает номер выбранного элемента

		:return int:
		"""
		Clear()
		for number in range(self.length):
			button = self.buttons[number]
			if number == self.selected:
				print(Back.WHITE+Fore.BLACK+button)
			else:
				print(button)
		key = ord(ReadKey())
		if key == 224:
			key = ord(ReadKey())
		Clear()
		if key == 80:
			if self.selected == self.length-1:
				self.selected = 0
			else:
				self.selected += 1

		elif key == 72:
			if self.selected == 0:
				self.selected = self.length-1
			else:
				self.selected -= 1

		elif key == 13:
			Sleep(.2)
			Clear()
			return self.selected


		return Menu.select(self)


class Product:
	"""
	Объект товара
	"""
	def __init__(self, name: str, desc: str, provider: str, price: float, count: int):
		"""
		Конструктор объекта товара
		"""
		self.name = name
		self.desc = desc
		self.provider = provider
		self.price = price
		self.count = count

class User:
	"""
	Класс пользователя.
	Поддерживает конструктор.
	В классе хранятся методы, которые пользователь может выполнять
	"""
	def __init__(self, login: str, password: str, lvl: int):
		"""
		Конструктор класса пользователя
		"""
		self.login = login
		self.password = password
		self.lvl = lvl
	class method:
		"""
		Класс со всеми методами для пользователей
		"""
		def __init__(self, user: object):
			"""
			Конструктор класса с методами

			:param user: - Объект пользователя
			"""
			self.user = user
		def _tabulate_products(self, products: list):
			"""
			Вспомогательная функция.
			Возвращает преобразованный в табличный вид
			список товаров

			:param products: - список словарей товаров
			:return str:
			"""
			headers = ["Наименование", "Описание", "Поставщик", "Цена", "Количество"]
			data = []
			for prod in products:
				data.append((prod['name'], prod['desc'], prod['provider'], prod['price'], prod['count']))
			return tabulate(data,headers,tablefmt="grid")

		def show_products(self):
			"""
			Функция выводит список всех товаров
			"""
			with open('products.json', encoding='ISO-8859-1') as f:
				products = json.loads(f.read())
			print(self._tabulate_products(products))
			input("Нажмите Enter чтобы закрыть это окно")

		def get_products(self):
			"""
			Функция возвращает объекты всех товаров

			:return list: 
			"""
			with open('products.json', encoding='ISO-8859-1') as f:
				products = json.loads(f.read())
			response = []
			product_id = 0
			for product in products:
				response.append(Product(product['name'], product['desc'], product['provider'], float(product['price']), int(product['count'])))
				product_id+=1

			return response
		def get_methods(self):
			"""
			Функция возвращает список доступных методов для пользователя

			:return list:
			"""
			functions = []
			if self.user.lvl == 1:
				functions = ['Show products', 'Edit product', 'Add product', 'Remove product', 'Exit']
			else:
				functions = ['Show products', 'Exit']

			return functions

		def _rewrite_products(self, products: list):
			"""
			Вспомогательная функция, которая обновляет список товаров

			:param products: - список объектов товаров
			"""
			products_to_dict = []
			for i in products:
				products_to_dict.append({
					'name':i.name,
					'desc':i.desc,
					'provider':i.provider,
					'price':i.price,
					'count':i.count
					})

			with open('products.json', 'w') as f:
				f.write(json.dumps(products_to_dict, ensure_ascii=False, indent=2, sort_keys=True))

		def generate_product(self):
			"""
			Функция - генератор объекта продукта

			:return Product:
			"""
			name = input("Наименование нового продукта: ")
			desc = input("Описание нового продукта: ")
			provider = input("Поставщик нового продукта: ")
			price = input("Цена нового продукта: ")
			count = input("Количество нового продукта: ")

			if count.isnumeric() and price.replace('.','',1).isnumeric():
				return Product(
						name,
						desc,
						provider,
						float(price),
						int(count)
					)
			else:
				print("Error while inputing data: price and count must be numeric")
		def remove_product(self, product: Product):
			"""
			Функция для удаления товара

			:param product: - объект товара, который необходимо удалить
			"""
			products = self.get_products()
			products.pop(product)
			print(products)
			self._rewrite_products(products)
		def add_product(self, product: Product):
			"""
			Функция для добавления нового товара

			:param product: - объект товара, который необходимо добавить
			"""
			products = self.get_products()
			products.append(product)
			self._rewrite_products(products)

		def edit_product(self, product_id: int):
			"""
			Функция для редактирования полей товара

			:param product_id: - порядковый номер товара
			"""
			products = self.get_products()
			product_to_edit = products[product_id]
			buttons = [
				"Наименование",
				"Описание",
				"Поставщик",
				"Цена",
				"Количество"
			]
			menu = Menu(buttons)
			action = menu.select()
			new_value = input(f"Введите новое значение для пункта <{buttons[action]}>:\n")
			match action:
				case 0:
					product_to_edit.name = new_value
				case 1:
					product_to_edit.desc = new_value
				case 2:
					product_to_edit.desc = new_value
				case 3:
					product_to_edit.desc = new_value
				case 4:
					if new_value.isnumeric():
						product_to_edit.count = new_value
					else:
						print("Inputed data is not numeric")

			products[product_id] = product_to_edit
			self._rewrite_products(products)


class Auth:
	def auth(self):
		auth_type = Menu(['Регистрация', 'Вход в аккаунт']).select()
		try:
			if auth_type == 0:
				print("Registration")
				login = input('login: ')
				passwd = input('passwd: ')
				retyped = input('retype passwd: ')
				user = self.signup(login, passwd, retyped)
				

			else:
				print("Logging in")
				login = input('login: ')
				passwd = input('passwd: ')
				user = self.login(login, passwd)
			return user
		except ProjectExceptions.AuthError.InvalidLogin as exception:
			print(f"Ошибка логина: {exception}")
		except ProjectExceptions.AuthError.InvalidPassword as exception:
			print(f"Ошибка пароля: {exception}")
		Sleep(1.5)
		return self.auth()
	def _get_accounts(self):
		"""
		Вспомогательная функция.
		Возвращает словарь пользователей

		:return dict:
		"""
		with open('users.json', encoding='ISO-8859-1') as f:
			return json.loads(f.read())

	def _reg_account(self, login: str, password: str, lvl: int = 0):
		"""
		Функция позволяет добавить нового пользователя в базу

		:param login: - логин пользователя
		:param password: - пароль пользователя
		:param lvl: - уровень пользователя (по умолчанию 0)
		"""
		users = Auth._get_accounts(self)
		users[login] = {'password':password, 'lvl':lvl}
		with open('users.json', 'w') as f:
			f.write(json.dumps(users, ensure_ascii=False))
	def login(self, login: str, password: str) -> User:
		"""
		Функция авторизации, принимает на вход логин и пароль
		Возвращает объект пользователя, если тот есть в базе,
		в ином случае вызывает исключение

		:param login: - логин пользователя
		:param password: - пароль пользователя
		:return User:
		"""
		accounts = Auth._get_accounts(self)
		if login not in accounts:
			raise ProjectExceptions.AuthError.InvalidLogin("Login is invalid")
		elif accounts[login]['password'] != password:
			raise ProjectExceptions.AuthError.InvalidPassword("Password is invalid")
		else:
			lvl = accounts[login]['lvl']
			return User(login, password, lvl)

	def signup(self, login: str, password: str, retyped_password: str) -> User:
		"""
		Функция регистрации, принимает на вход логин и пароль
		Возвращает объект пользователя, если такого же логина
		нет в базе, в ином случае вызывает исключение

		:param login: - Логин пользователя
		:param password: - Пароль пользователя
		:param retyped_password: - Повтор пароля пользователя

		:return User:
		"""
		accounts = Auth._get_accounts(self)
		if login in accounts:
			raise ProjectExceptions.AuthError.InvalidLogin('User with this login already exists')
		elif password != retyped_password:
			raise ProjectExceptions.AuthError.InvalidPassword('Entered passwords must be same')
		else:
			Auth._reg_account(self,login,password,0)
			return User(login, password, 0)