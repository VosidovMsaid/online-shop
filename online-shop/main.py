try:
	import telebot
	import config as cnf
	import function as func
	from telebot import types
	import lang.ru as ru 
	import lang.tj as tj
except:
	import os
	os.system("pip install mysql-connector-python pyTelegramBotAPI")
bot = telebot.TeleBot(cnf.TOKEN)


# COMMENT
def comment(message):
	userId = message.from_user.id
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		markup.row(back)
		bot.send_message(message.chat.id, ru.comment_text, reply_markup=markup)
		bot.register_next_step_handler(message, comment_text)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		markup.row(back)
		bot.send_message(message.chat.id, tj.comment_text, reply_markup=markup)
		bot.register_next_step_handler(message, comment_text)
def comment_text(message):
	userId = message.from_user.id
	username = message.from_user.username

	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	global message_text
	message_text=message.text

	if message_text == ru.back or message.text == tj.back:
		send_welcome(message)
	else:
		create_order = "INSERT INTO comments (userId, username, message) VALUES (%s, %s, %s)"
		values = (userId, username, message_text)
		func.execute_query(connection, create_order, values)

		get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
		if get_lang[0] == "ru":
			bot.send_message(message.chat.id, ru.comment_thanks)
			send_welcome(message)
		else:
			bot.send_message(message.chat.id, tj.comment_thanks)
			send_welcome(message)

# EDIT NAME
def edit_name(message):
	userId = message.from_user.id
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		markup.row(back)
		bot.send_message(message.chat.id, ru.your_fio, reply_markup=markup)
		bot.register_next_step_handler(message, edit_name1)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		markup.row(back)
		bot.send_message(message.chat.id, tj.your_fio, reply_markup=markup)
		bot.register_next_step_handler(message, edit_name1)

def edit_name1(message):
	userId = message.from_user.id
	username = message.from_user.username

	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	global fio_edit
	fio_edit=message.text

	if fio_edit == ru.back or fio_edit == tj.back:
		my_profile(message)
	else:
		split_fio = fio_edit.split()
		if len(split_fio)==2:
			sql = "UPDATE users SET firstname = %s, lastname=%s WHERE userId = %s"
			val = (split_fio[0], split_fio[1], userId)
			users = func.execute_query(connection, sql, val) 

			get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
			if get_lang[0] == "ru":
				bot.send_message(message.chat.id, ru.thank_edit_fio)
				send_welcome(message)
			else:
				bot.send_message(message.chat.id, tj.thank_edit_fio)
				send_welcome(message)
		else:
			get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
			if get_lang[0] == "ru":
				bot.send_message(message.chat.id, "Неправильный ввод (Имя и фамилия)")
			else:
				bot.send_message(message.chat.id, "Маълумотро нодуруст дохил кардед (Ном ва насаб)")
			edit_name(message)


# EDIT PHONE
def edit_phone(message):
	userId = message.from_user.id
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		markup.row(back)
		bot.send_message(message.chat.id, ru.your_phone, reply_markup=markup)
		bot.register_next_step_handler(message, edit_phone1)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		markup.row(back)
		bot.send_message(message.chat.id, tj.your_phone, reply_markup=markup)
		bot.register_next_step_handler(message, edit_phone1)

def edit_phone1(message):
	userId = message.from_user.id
	username = message.from_user.username

	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	global phone_edit
	phone_edit=message.text

	if phone_edit == ru.back or phone_edit == tj.back:
		my_profile(message)
	else:
		if phone_edit.isdigit() and len(phone_edit)<=9:
			sql = "UPDATE users SET phone_number = %s WHERE userId = %s"
			val = (phone_edit, userId)
			users = func.execute_query(connection, sql, val) 

			get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
			if get_lang[0] == "ru":
				bot.send_message(message.chat.id, ru.thank_edit_phone)
				send_welcome(message)
			else:
				bot.send_message(message.chat.id, tj.thank_edit_phone)
				send_welcome(message)
		else:
			get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
			if get_lang[0] == "ru":
				bot.send_message(message.chat.id, "Неправильный ввод (+992 XXXXXXXXX)")
			else:
				bot.send_message(message.chat.id, "Маълумотро нодуруст дохил кардед (+992 XXXXXXXXX)")
			edit_phone(message)


# EDIT ADDRESS 
def edit_address(message):
	userId = message.from_user.id
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(ru.back)
		markup.row(back)
		bot.send_message(message.chat.id, ru.your_address, reply_markup=markup)
		bot.register_next_step_handler(message, edit_address1)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton(tj.back)
		markup.row(back)
		bot.send_message(message.chat.id, tj.your_address, reply_markup=markup)
		bot.register_next_step_handler(message, edit_address1)

def edit_address1(message):
	userId = message.from_user.id
	username = message.from_user.username

	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	global address_edit
	address_edit=message.text

	if address_edit == ru.back or address_edit == tj.back:
		my_profile(message)
	else:
		
		sql = "UPDATE users SET address = %s WHERE userId = %s"
		val = (address_edit, userId)
		users = func.execute_query(connection, sql, val) 

		get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
		if get_lang[0] == "ru":
			bot.send_message(message.chat.id, ru.thank_edit_address)
			send_welcome(message)
		else:
			bot.send_message(message.chat.id, tj.thank_edit_address)
			send_welcome(message)

# CART
def cart(message):
	userId = message.from_user.id
	func.update_pipeline(message, pipeline=9)

	markup1=types.InlineKeyboardMarkup()
	orders = func.get_order_datas(message)
	mes = ""
	total_sum = 0
	for i in orders:
		mes+="🔹 " + str(i[2]) + f" 1 шт. - {str(i[3])} сомони\n" + " └ "+str(i[4]) + " x " + str(float(i[3])) + " = " + str(int(i[3])*int(i[4])) + " сомони\n"
		total_sum+=int(i[3])*int(i[4])

		minus=types.InlineKeyboardButton("➖", callback_data='decrease' + str(i[0]))
		cancel=types.InlineKeyboardButton("❌", callback_data='remove' + str(i[0]))
		plus=types.InlineKeyboardButton("➕", callback_data='increase' + str(i[0]))
		markup1.row(minus,cancel,plus)

	mes+=f"\nИтого: <b>{float(total_sum)} сомони</b>"

	bot.send_message(userId, mes, reply_markup=markup1, parse_mode="html")
	return mes, total_sum



def start_oformit_order(message):
	userId = message.from_user.id
	func.update_pipeline(message, pipeline=10)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	if get_lang[0] == "ru":
		oplata_order = types.KeyboardButton(ru.oplata_order)
		back = types.KeyboardButton(ru.back)
		markup.row(oplata_order)
		markup.row(back)
	else:
		oplata_order = types.KeyboardButton(tj.oplata_order)
		back = types.KeyboardButton(tj.back)
		markup.row(oplata_order)
		markup.row(back)

	orders = func.get_order_datas(message)
	mes = ""
	total_sum = 0
	mes+="Товары на заказ\n\n"
	for i in orders:
		mes+="🔹 " + str(i[2]) + f" 1 шт. - {str(i[3])} сомони\n" + " └ "+str(i[4]) + " x " + str(float(i[3])) + " = " + str(int(i[3])*int(i[4])) + " сомони\n"
		total_sum+=int(i[3])*int(i[4])

	mes+=f"\nПродукты: <b>{float(total_sum)} сомони</b>\nДоставка:  <b>Отсутствует</b>\nДля оплаты: <b>{float(total_sum)} сомони</b>"

	bot.send_message(userId, mes,reply_markup=markup, parse_mode="html")
	return mes


def oplata_order(message):
	userId = message.from_user.id
	func.update_pipeline(message, pipeline=11)
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if get_lang[0] == "ru":
		oplata_order = types.KeyboardButton(ru.nalichnie)
		back = types.KeyboardButton(ru.back)
		markup.row(oplata_order)
		markup.row(back)
		bot.send_message(message.chat.id, "Каким способом вы хотите оплатить заказ ?\n\n<i>Выберите один из следующих.</i>", reply_markup=markup, parse_mode="html")
	else:
		oplata_order = types.KeyboardButton(tj.nalichnie)
		back = types.KeyboardButton(tj.back)
		markup.row(oplata_order)
		markup.row(back)
		bot.send_message(message.chat.id, "Шумо чӣ гуна мехоҳед барои фармоиш пардохт кунед?\n\n<i>Яке аз имконоти зеринро интихоб кунед.</i>", reply_markup=markup,parse_mode="html")


def add_all_products_to_cart(message, products, price):
	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	userId = message.from_user.id 
	username = str(message.from_user.username)
	get_profile_data = func.get_profile(message)

	create_order = "INSERT INTO cart (userId, username, phone_number, address, orders, price, paid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	values = (userId, username, get_profile_data['phone'], get_profile_data['address'], products, price, False)
	func.execute_query(connection, create_order, values)



def delete_orders_from_shopping_cart(message):
	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	userId = message.from_user.id 

	mycursor = connection.cursor()

	sql = "DELETE FROM shopping_cart WHERE userId = '{userId}'".format(userId=userId)

	mycursor.execute(sql)

	connection.commit()





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		orders = func.get_order_datas(call)
		for i in orders:
			if call.data == 'remove'+ str(i[0]):
				connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
				myprod = connection.cursor()
				sql = "DELETE FROM shopping_cart WHERE id = '{id}'".format(id=i[0])
				myprod.execute(sql)
				connection.commit()

				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
				cart(call)


			if call.data == 'decrease'+str(i[0]):
				total=int(i[4])
				total-=1
				connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
				myprod = connection.cursor()
				sql = """UPDATE shopping_cart SET amount = "{amount}" WHERE product="{row}" """.format(amount=total,row=i[2])
				myprod.execute(sql)
				connection.commit()

				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
				cart(call)

			if call.data == 'increase'+str(i[0]):
				total=int(i[4])
				total+=1
				connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
				myprod = connection.cursor()
				sql = """UPDATE shopping_cart SET amount = "{amount}" WHERE product="{row}" """.format(amount=total,row=i[2])
				myprod.execute(sql)
				connection.commit()

				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
				cart(call)





@bot.message_handler(commands=['start'])
def send_welcome(message):
	userId = message.from_user.id
	username = str(message.from_user.username)
	if userId in func.db_users("userId"):
		print(f"User found - {userId} - {username}")
	else:
		func.create_user_pipeline(message)
	
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	print(get_lang)
	func.main_buttons(message, lang=get_lang[0])
	func.update_pipeline(message, pipeline=1)




def amount_buttons(message):
	userId = message.from_user.id
	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)


	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if get_lang[0] == "ru":
		to_menu = types.KeyboardButton(ru.to_menu)
		cart = types.KeyboardButton(ru.cart)
	else:
		to_menu = types.KeyboardButton(tj.to_menu)
		cart = types.KeyboardButton(tj.cart)
	markup.row(to_menu, cart)

	btn1 = types.KeyboardButton("1")
	btn2 = types.KeyboardButton("2")
	btn3 = types.KeyboardButton("3")
	btn4 = types.KeyboardButton("4")
	btn5 = types.KeyboardButton("5")
	btn6 = types.KeyboardButton("6")
	btn7 = types.KeyboardButton("7")
	btn8 = types.KeyboardButton("8")
	btn9 = types.KeyboardButton("9")
	markup.row(btn1, btn2, btn3)
	markup.row(btn4, btn5, btn6)
	markup.row(btn7, btn8, btn9)

	if get_lang[0] == "ru":
		bot.send_message(message.chat.id, ru.write_amount, reply_markup=markup)
		bot.register_next_step_handler(message, set_amount)
	else:
		bot.send_message(message.chat.id, tj.write_amount, reply_markup=markup)
		bot.register_next_step_handler(message, set_amount)

def set_amount(message):
	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)

	userId = message.from_user.id
	global amount_count
	amount_count = message.text

	if amount_count == ru.to_menu or amount_count == tj.to_menu:
		func.category_list(message)
	elif amount_count == ru.cart or amount_count == tj.cart:
		print("Cart")

	else:
		sql = "UPDATE pipeline SET amount = %s WHERE userId = %s"
		val = (amount_count, userId)
		users = func.execute_query(connection, sql, val) 

		get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
		get_product = func.db_pipeline_by_user(message, column="product", user=userId)[0]
		gett = func.get_product_inf(message, product_name=get_product)

		create_cart = "INSERT INTO shopping_cart (userId, product, price, amount) VALUES (%s, %s, %s, %s)"
		values = (userId, gett['name'], gett['price'], amount_count)
		func.execute_query(connection, create_cart, values) 

		
		if get_lang[0] == "ru":
			bot.send_message(message.chat.id, f"✅ {gett['name']} 1 шт. от {amount_count} добавлен в корзину.\n\nЕсли вы хотите заказать что-то ещё, продолжите заказывать или вы можете оформить заказ, перейдя в корзину.")
			func.category_list(message)
		else:
			bot.send_message(message.chat.id, f"✅ {gett['name']} - {amount_count} дона ба сабад ворид шуд.\n\nАгар шумо хоҳед, ки чизи дигарро фармоиш диҳед, фармоишро идома диҳед ё шумо метавонед бо рафтан ба аробаи харид пардохт кунед.")
			func.category_list(message)

def oplata_nalichnie(message):
	userId = message.from_user.id
	get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)

	orders = func.get_order_datas(message)
	mes = ""
	total_sum = 0
	for i in orders:
		mes+=str(i[2])+" - " + str(i[4]) + " шт. x " + str(float(i[3]))+"\n"
		total_sum+=int(i[3])*int(i[4])
	add_all_products_to_cart(message, mes, total_sum)
	delete_orders_from_shopping_cart(message)


	if get_lang[0] == "ru":
		bot.send_message(message.chat.id, "Заказ принят и отправлен на рассмотрение модераторам.")
		send_welcome(message)
	else:
		bot.send_message(message.chat.id, "Фармоиш қабул ва барои баррасӣ ба модераторҳо фиристода шуд.")
		send_welcome(message)

@bot.message_handler(content_types=['text'])
def echo_text(message):
	userId = message.from_user.id
	get_pipeline = func.db_pipeline_by_user(message, column="pipeline", user=userId)
	get_pipeline = get_pipeline[0]

	if message.text == ru.back or message.text == tj.back:
		if get_pipeline==2 or get_pipeline==3 or get_pipeline==4 or get_pipeline==6:
			get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
			func.main_buttons(message, lang=get_lang[0])
		if get_pipeline==5:
			func.my_profile(message)
		if get_pipeline==7:
			func.category_list(message)

		if get_pipeline==10:
			func.cart_message(message)
			cart(message)
		if get_pipeline==11:
			start_oformit_order(message)

	if message.text == ru.to_menu or message.text == tj.to_menu:
		func.category_list(message)

	if message.text == ru.about_us or message.text == tj.about_us and get_pipeline==1:
		bot.send_message(message.chat.id, func.about_us(message))

	if message.text == ru.lang or message.text == tj.lang and get_pipeline==1:
		func.update_pipeline(message, pipeline=2)
		func.language(message)

	if message.text == ru.lang_ru and get_pipeline==2:
		func.update_lang(message, "ru")
		get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
		bot.send_message(message.chat.id, "Язык изменен!")
		func.main_buttons(message, lang=get_lang[0])
		

	if message.text == tj.lang_tj and get_pipeline==2:
		func.update_lang(message, "tj")
		get_lang = func.db_pipeline_by_user(message, column="lang", user=userId)
		bot.send_message(message.chat.id, "Забон иваз карда шуд!")
		func.main_buttons(message, lang=get_lang[0])


	if message.text == tj.comment or message.text == ru.comment:
		func.update_pipeline(message, pipeline=3)
		comment(message)

	if message.text == ru.my_profile or message.text == tj.my_profile and get_pipeline==1:
		func.update_pipeline(message, pipeline=4)
		func.my_profile(message)

	if message.text == ru.edit_name or message.text == tj.edit_name and get_pipeline==4:
		func.update_pipeline(message, pipeline=5)
		edit_name(message)

	if message.text == ru.edit_phone or message.text == tj.edit_phone and get_pipeline==4:
		func.update_pipeline(message, pipeline=5)
		edit_phone(message)

	if message.text == ru.edit_address or message.text == tj.edit_address and get_pipeline==4:
		func.update_pipeline(message, pipeline=5)
		edit_address(message)

	if message.text == ru.start_order or message.text == tj.start_order and get_pipeline==1:
		func.category_list(message)

	connection = func.create_connection(cnf.host, cnf.username, cnf.password, cnf.database)
	select_category = "SELECT name from category"
	categories = func.execute_read_query(connection, select_category)
	categories = [t[0] for t in categories]

	for i in categories:
		if message.text == i:
			func.update_pipeline(message, pipeline=7)
			func.get_products(message, message.text)

	select_product = "SELECT name from products"
	products = func.execute_read_query(connection, select_product)
	products = [t[0] for t in products]

	for j in products:
		if message.text == j:
			func.update_pipeline(message, pipeline=8)
			get_info_product = func.get_product_inf(message, message.text)
	


	select_amount = "SELECT price FROM pipeline WHERE userId = {userId}".format(userId=userId)
	amount = func.execute_read_query(connection, select_amount)

	for b in amount:
		for bb in b:
			if message.text == f"1 шт. - {bb} сомони":
				amount_buttons(message)


	if message.text == ru.cart or message.text == tj.cart:
		func.cart_message(message)
		cart(message)

	if message.text == ru.start_oformit_order or message.text == tj.start_oformit_order and get_pipeline==9:
		start_oformit_order(message)

	if message.text == ru.oplata_order or message.text == tj.oplata_order and get_pipeline==10:
		oplata_order(message)

	if message.text == ru.nalichnie or message.text == tj.nalichnie and get_pipeline==11:
		oplata_nalichnie(message)

	if message.text == ru.my_orders or message.text == tj.my_orders and get_pipeline==1:
		for i in func.my_orders(message):
			bot.send_message(message.chat.id, i, parse_mode="html")


bot.infinity_polling()
