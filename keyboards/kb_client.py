from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


DELKB = ReplyKeyboardRemove() # удаляем клавиатуру

b1 = KeyboardButton('/Оформить_заказ')
b2 = KeyboardButton('/Информация_по_оформленному_заказ')
b3 = KeyboardButton('/График_работы')
b4 = KeyboardButton('/Написать_оператору')

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)

# .add() - одна кнопка в списке, insert() - добавляет в список к первому
# .row() - все в строку
client_kb.add(b1).add(b2).add(b3).insert(b4)

'''Инлайн клавиатура главное меню'''
ib1 = KeyboardButton('🟢 Оформить заказ')
ib2 = KeyboardButton('❓ Информация по оформленному заказу')
ib3 = KeyboardButton('⏱ График работы')
ib4 = KeyboardButton('📩 Написать оператору')

inclient_kb = ReplyKeyboardMarkup(resize_keyboard=True)
inclient_kb.add(ib1).add(ib2).add(ib3).insert(ib4)

'''Инлайн клавиатура выбор как узнать статус заказа'''
# Order_Menu = InlineKeyboardMarkup(row_width=2) # для вызова вставляем в код reply_markup=Order_Menu
# ob1 = InlineKeyboardButton(text='По номеру заказа', callback_data='По номеру заказа')
# ob2 = InlineKeyboardButton(text='По номеру телефона', callback_data='По номеру телефона')
# Order_Menu.insert(ob1, ob2)

