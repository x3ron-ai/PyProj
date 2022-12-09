import json
from utils import *
Clear()
App = Auth()

user = App.auth()
Method = user.method(user)

methods = Method.get_methods()

while True:
	Sleep(.2)
	Clear()
	action = Menu(methods).select()
	if methods[action] == 'Show products':
		Method.show_products()
	elif methods[action] == 'Edit product':
		products = [i.name for i in Method.get_products()]
		product_id = Menu(products).select()
		Method.edit_product(product_id)
	elif methods[action] == 'Add product':
		product = Method.generate_product()
		Method.add_product(product)
		print("Добавлен успешно!")
		Sleep(.2)
	elif methods[action] == 'Exit':
		exit(1)