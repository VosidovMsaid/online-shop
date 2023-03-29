try:
	import mysql.connector
	from mysql.connector import Error
	import config as cnf
	from telebot import types
	import lang.ru as ru 
	import lang.tj as tj
	import telebot
	from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

except:
	import os
	os.system("pip install mysql-connector-python pyTelegramBotAPI")

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def db_users(column=""):
	l=[]
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_users = "SELECT {column} from users".format(column=column)
	users = execute_read_query(connection, select_users)
	for i in users:
		for j in i:
			l.append(j)
	return l


def create_user(message):
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	userId = message.from_user.id 
	username = str(message.from_user.username)
	firstname = str(message.from_user.first_name)
	lastname = str(message.from_user.last_name)

	create_users = "INSERT INTO users (userId, username, firstname, lastname, phone_number, address, orders_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	values = (userId, username, firstname, lastname, "-", "-", 0)
	execute_query(connection, create_users, values) 
	print( f"User created - {userId} - {username}" )


def create_pipeline(message):
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	userId = message.from_user.id 
	username = str(message.from_user.username)

	create_users = "INSERT INTO pipeline (userId, username, pipeline, lang, product, price, amount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	values = (userId, username, 0, "ru", None, None, 0)
	execute_query(connection, create_users, values) 


def create_user_pipeline(message):
	create_user(message)
	create_pipeline(message)


def db_pipeline_by_user(message, column="", user=0):
	userId = message.from_user.id
	l=[]
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_users = "SELECT {column} FROM pipeline WHERE userId = {userId}".format(column=column, userId=userId)
	users = execute_read_query(connection, select_users)
	for i in users:
		for j in i:
			l.append(j)

	return l


def update_pipeline(message, pipeline=0):
	userId = message.from_user.id
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	sql = "UPDATE pipeline SET pipeline = %s WHERE userId = %s"
	val = (pipeline, userId)
	users = execute_query(connection, sql, val)

bot = telebot.TeleBot(cnf.TOKEN)
@bot.message_handler(commands=['start'])
def main_buttons(message, lang=""):
	update_pipeline(message, pipeline=1)
	if lang=="ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		start_order = types.KeyboardButton(ru.start_order)
		my_profile = types.KeyboardButton(ru.my_profile)
		my_orders = types.KeyboardButton(ru.my_orders)
		language = types.KeyboardButton(ru.lang)
		about_us = types.KeyboardButton(ru.about_us)
		comment = types.KeyboardButton(ru.comment)
		markup.row(start_order)
		markup.row(my_profile, my_orders)
		markup.row(language, about_us)
		markup.row(comment)
		bot.send_message(message.chat.id,"Здравствуйте, Вас приветствует бот ____________.\n⏰ Время работы с 9:00 до 23:30\n\nСуши бар работает с 12:00 до 23:30\n🛒 Вы можете заказать через наш бот. Или по номеру +992(92) 000-00-00" , reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		start_order = types.KeyboardButton(tj.start_order)
		my_profile = types.KeyboardButton(tj.my_profile)
		my_orders = types.KeyboardButton(tj.my_orders)
		language = types.KeyboardButton(tj.lang)
		about_us = types.KeyboardButton(tj.about_us)
		comment = types.KeyboardButton(tj.comment)
		markup.row(start_order)
		markup.row(my_profile, my_orders)
		markup.row(language, about_us)
		markup.row(comment)
		bot.send_message(message.chat.id,"Салом, Хуш омадед ба бот ____________.\n⏰ Соатҳои корӣ аз 9:00 то 23:30\n\nСуши-бар аз 12:00 то 23:30 кор мекунад\n🛒 Шумо метавонед тавассути боти мо фармоиш диҳед. Ё ба рақами +992(92) 000-00-00 занг занед" , reply_markup=markup)


def about_us(message):
	userId = message.from_user.id
	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		return ru.about_us
	else:
		return tj.about_us

@bot.message_handler(content_types=['text'])
def language(message):
	userId = message.from_user.id
	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		rus = types.KeyboardButton(ru.lang_ru)
		tjk = types.KeyboardButton(tj.lang_tj)
		markup.row(back)
		markup.row(rus, tjk)
		bot.send_message(message.chat.id, ru.choose_lang, reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		rus = types.KeyboardButton(ru.lang_ru)
		tjk = types.KeyboardButton(tj.lang_tj)
		markup.row(back)
		markup.row(rus, tjk)
		bot.send_message(message.chat.id, tj.choose_lang, reply_markup=markup)


def update_lang(message, lang=""):
	userId = message.from_user.id
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	sql = "UPDATE pipeline SET lang = %s WHERE userId = %s"
	val = (lang, userId)
	users = execute_query(connection, sql, val)

def get_profile(message):
	userId = message.from_user.id
	l=[]
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_users = "SELECT firstname, lastname, address, phone_number, date_of_register  FROM users WHERE userId = {userId}".format(userId=userId)
	users = execute_read_query(connection, select_users)

	for i in users:
		for j in i:
			l.append(j)

	dic_user = {
		"firstname": l[0],
		"lastname": l[1],
		"phone": l[3],
		"address": l[2],
		"datetime": l[4].strftime('%Y-%m-%d %H:%M:%S')
	}
	return dic_user


def my_profile(message):
	userId = message.from_user.id
	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		profile_datas = get_profile(message)

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		edit_name = types.KeyboardButton(ru.edit_name)
		edit_address = types.KeyboardButton(ru.edit_address)
		edit_phone = types.KeyboardButton(ru.edit_phone)
		markup.row(back, edit_name)
		markup.row(edit_address, edit_phone)
		profile = "Ваш профиль:\n\n👤 Имя и фамилия: <b>{firstname} {lastname}</b>\n📱 Телефон: <b>{phone}</b>\n📍 Адрес: <b>{address}</b>\n       Дата регистрации: <b>{datetime}</b>".format(firstname=profile_datas["firstname"], lastname=profile_datas["lastname"], phone=profile_datas["phone"], address=profile_datas["address"], datetime=profile_datas["datetime"])
		bot.send_message(message.chat.id, profile, reply_markup=markup, parse_mode="html")
		bot.send_message(message.chat.id, ru.edit_profile_text)
	else:
		profile_datas = get_profile(message)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		edit_name = types.KeyboardButton(tj.edit_name)
		edit_address = types.KeyboardButton(tj.edit_address)
		edit_phone = types.KeyboardButton(tj.edit_phone)
		markup.row(back, edit_name)
		markup.row(edit_address, edit_phone)
		profile = "Профили шумо:\n\n👤 Ному насаб: <b>{firstname} {lastname}</b>\n📱 Рақами телефон: <b>{phone}</b>\n📍 Суроға: <b>{address}</b>\n       Санаи бақайдгирӣ: <b>{datetime}</b>".format(firstname=profile_datas["firstname"], lastname=profile_datas["lastname"], phone=profile_datas["phone"], address=profile_datas["address"], datetime=profile_datas["datetime"])
		bot.send_message(message.chat.id, profile, reply_markup=markup, parse_mode="html")
		bot.send_message(message.chat.id, tj.edit_profile_text)


def category_list(message):
	update_pipeline(message, pipeline=6)
	userId = message.from_user.id
	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if get_lang[0] == "ru":
		back = types.KeyboardButton(ru.back)
		cart = types.KeyboardButton(ru.cart)
	else:
		back = types.KeyboardButton(tj.back)
		cart = types.KeyboardButton(tj.cart)
	markup.row(back, cart)
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_category = "SELECT name from category"
	categories = execute_read_query(connection, select_category)
	categories = [t[0] for t in categories]

	if len(categories)%2==0:
		result = [categories[i:i+2] for i in range(0, len(categories)-1, 2)]
	else:
		result = [categories[i:i+2] for i in range(0, len(categories)-1, 2)]
		result.append([categories[-1]])
	for sublist in result:
	    row = []
	    for item in sublist:
	        button = KeyboardButton(text=item)
	        row.append(button)

	    markup.add(*row)

	if get_lang[0] == "ru":
		bot.send_message(message.chat.id, ru.select_category, reply_markup=markup)
	else:
		bot.send_message(message.chat.id, tj.select_category, reply_markup=markup)


def get_products(message, category_name):
	userId = message.from_user.id
	select_category = "SELECT name FROM products WHERE category = '{cat}'".format(cat=category_name)
	categories = execute_read_query(connection, select_category)

	l=[]
	for i in categories:
		for j in i:
			l.append(j)

	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if get_lang[0] == "ru":
		back = types.KeyboardButton(ru.back)
		cart = types.KeyboardButton(ru.cart)
	else:
		back = types.KeyboardButton(tj.back)
		cart = types.KeyboardButton(tj.cart)
	markup.row(back, cart)


	if len(l)%2==0:
		result = [l[i:i+2] for i in range(0, len(l)-1, 2)]
	else:
		result = [l[i:i+2] for i in range(0, len(l)-1, 2)]
		result.append([l[-1]])
	for sublist in result:
	    row = []
	    for item in sublist:
	        button = KeyboardButton(text=item)
	        row.append(button)

	    markup.add(*row)

	bot.send_message(message.chat.id, message.text, reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_product_inf(message, product_name):
	userId = message.from_user.id
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_product_info = "SELECT name, photo, price, description, amount FROM products WHERE name = '{name}'".format(name=product_name)
	product_info = execute_read_query(connection, select_product_info)

	product_info_list = []
	for i in product_info:
		for j in i:
			product_info_list.append(j)

	dic = {
		'name': product_info_list[0],
		'photo': product_info_list[1],
		'price': product_info_list[2],
		'description': product_info_list[3],
		'amount': product_info_list[4]
	}

	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if get_lang[0] == "ru":
		to_menu = types.KeyboardButton(ru.to_menu)
		cart = types.KeyboardButton(ru.cart)
	else:
		to_menu = types.KeyboardButton(tj.to_menu)
		cart = types.KeyboardButton(tj.cart)
	markup.row(to_menu, cart)

	price_product = types.KeyboardButton(f"1 шт. - {dic['price']} сомони")
	markup.row(price_product)
	response = f"<a href='{dic['photo']}'>&#8205;</a><b>{dic['name']}</b>\n\n<i>{dic['description']}</i>"
	bot.send_message(message.chat.id, response, parse_mode="html", reply_markup=markup)
	
	userId = message.from_user.id
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	sql = "UPDATE pipeline SET product = %s WHERE userId = %s"
	val = (dic['name'], userId)
	users = execute_query(connection, sql, val)

	sql1 = "UPDATE pipeline SET price = %s WHERE userId = %s"
	val1 = (dic['price'], userId)
	users = execute_query(connection, sql1, val1)

	return dic

def get_order_datas(message):
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	userId = message.from_user.id
	select_orders = "SELECT * FROM shopping_cart WHERE userId = '{userId}'".format(userId=userId)
	orders = execute_read_query(connection, select_orders)

	return orders

def cart_message(message):
	userId = message.from_user.id
	update_pipeline(message, pipeline=9)

	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	if get_lang[0] == "ru":
		to_menu = types.KeyboardButton(ru.to_menu)
		start_oformit_order = types.KeyboardButton(ru.start_oformit_order)
		markup.row(start_oformit_order)
		markup.row(to_menu)
		bot.send_message(message.chat.id, ru.cart_send, reply_markup=markup)
	else:
		to_menu = types.KeyboardButton(tj.to_menu)
		start_oformit_order = types.KeyboardButton(tj.start_oformit_order)
		markup.row(start_oformit_order)
		markup.row(to_menu)
		bot.send_message(message.chat.id, tj.cart_send, reply_markup=markup)


def my_orders(message):
	userId = message.from_user.id
	connection = create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	get_lang = db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	
	ok=[]
	if get_lang[0] == "ru":
		select_orders = "SELECT * FROM cart WHERE userId = '{userId}'".format(userId=userId)
		orders = execute_read_query(connection, select_orders)
		for i in range(len(orders)):
			for j in range(len(orders[i])):

				if orders[i][7]==0:
					my_orders = """номер заказа: <b>{id}</b>\nСтатус: <b>Заказан</b>\nАдрес: <b>{address}</b>\nДата: <b>{datetime}</b>\n\n🔹 {products} = {sum} сомони\n\nСпособ оплаты: <b>💰 Наличные</b>\n\nДля продукта: <b>{sum} сомони</b>\nДля доставки:  <b>Отсутствует</b>\nОплачено: <b>Нет</b>\nЗаказ был принят модератором ? Жду ответа !!!""".format(id=orders[i][0], address=orders[i][4], datetime=orders[i][8], products=orders[i][5], sum=orders[i][6])
					ok.append(my_orders)
					break
				else:
					my_orders = """номер заказа: <b>{id}</b>\nСтатус: <b>Заказан</b>\nАдрес: <b>{address}</b>\nДата: <b>{datetime}</b>\n\n🔹 {products} = {sum} сомони\n\nСпособ оплаты: <b>💰 Наличные</b>\n\nДля продукта: <b>{sum} сомони</b>\nДля доставки:  <b>Отсутствует</b>\nОплачено: <b>Да</b>\nЗаказ был принят модератором ? Жду ответа !!!""".format(id=orders[i][0], address=orders[i][4], datetime=orders[i][8], products=orders[i][5], sum=orders[i][6])
					ok.append(my_orders)
					break

	else:
		select_orders = "SELECT * FROM cart WHERE userId = '{userId}'".format(userId=userId)
		orders = execute_read_query(connection, select_orders)
		for i in range(len(orders)):
			for j in range(len(orders[i])):

				if orders[i][7]==0:
					my_orders = """раками фармоиш: <b>{id}</b>\nСтатус: <b>Фармуд</b>\nСурога: <b>{address}</b>\nСана: <b>{datetime}</b>\n\n🔹 {products} = {sum} сомон\n\nТарзи пардохт: <b>💰 Пули накд</b>\n\nБарои фармоиш: <b>{sum} сомон</b>\nБарои расонидани:  <b>Номаълум</b>\nПардохт: <b>Не</b>\nФармоиш аз ҷониби модератор қабул карда шуд? Интизори ҷавоб!!!""".format(id=orders[i][0], address=orders[i][4], datetime=orders[i][8], products=orders[i][5], sum=orders[i][6])
					ok.append(my_orders)
					break
				else:
					my_orders = """раками фармоиш: <b>{id}</b>\nСтатус: <b>Фармуд</b>\nСурога: <b>{address}</b>\nСана: <b>{datetime}</b>\n\n🔹 {products} = {sum} сомон\n\nТарзи пардохт: <b>💰 Пули накд</b>\n\nБарои фармоиш: <b>{sum} сомон</b>\nБарои расонидани:  <b>Номаълум</b>\nПардохт: <b>Ха</b>\nФармоиш аз ҷониби модератор қабул карда шуд? Интизори ҷавоб!!!""".format(id=orders[i][0], address=orders[i][4], datetime=orders[i][8], products=orders[i][5], sum=orders[i][6])
					ok.append(my_orders)
					break
	return ok