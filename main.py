from webbrowser import get
from aiogram.utils import executor
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from email import message
import os

from constant import ID_ADMIN_ECHO, TOKEN, URL_APP
from keyboards import inclient_kb, DELKB


storage = MemoryStorage()
bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage = storage)

async def on_startup(dp):
    await bot.set_webhook(URL_APP)

async def on_shutdown(dp):
    await bot.delete_webhook()


'''********************************* Основной код ****************************'''


@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id,(f'👋 Рад видеть Вас {message.from_user.full_name}! Воспользуйтесь меню ниже:'), reply_markup=inclient_kb)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: https://t.me/EcoListBot')


'''***************************** Кнопка Оформить заказ*******************'''

class FSMZakaz(StatesGroup):
    name_product = State()
    quantity = State()
    fio = State()
    city = State()
    telefon = State()

# Начало диалога перехода в машинное состояние
@dp.message_handler(commands=['Оформить'], state = None)
async def cm_start(message : types.Message):
    await FSMZakaz.name_product.set()
    await message.reply('Для оформления заказа напишите название товара:', reply_markup=DELKB)

# Ловим первый ответ и загружаем в словарь
@dp.message_handler(state = FSMZakaz.name_product)
async def load_name_product(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Товар'] = message.text
    await FSMZakaz.next()
    await message.reply('\nТеперь напишите количество (сколько шт) товара положить Вам в заказ:')

# Ловим второй ответ
@dp.message_handler(state = FSMZakaz.quantity)
async def load_quantity(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Количество'] = message.text
    await FSMZakaz.next()
    await message.reply('\nТеперь напишите фамилию и имя кто будет получать заказа:')

# Ловим третий ответ
@dp.message_handler(state = FSMZakaz.fio)
async def load_fio(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Имя'] = message.text
    await FSMZakaz.next()
    await message.reply('\nТеперь напишите Ваш город и улицу:')

# Ловим четверты ответ 
@dp.message_handler(state = FSMZakaz.city)
async def load_city(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Адрес'] = message.text
    await FSMZakaz.next()
    await message.reply('\nТеперь напишите Ваш мобильный номер телефона:')

# Ловим последний ответ
@dp.message_handler(state = FSMZakaz.telefon)
async def load_telefon(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Телефон'] = message.text
    await message.reply('Заказ принят!\n\nМенеджер оформит заказ и свяжется с Вами в ближайшее время!\nОстались вопросы или хотите оформить новый заказ - воспользуйтесь меню!', reply_markup=inclient_kb)
    async with state.proxy() as data:
        await bot.send_message(chat_id=ID_ADMIN_ECHO,text=(message.from_user.full_name, message.from_user.id, str(data)))
    await state.finish()


''' *************************** Машинное состояние Информация по заказу ******************'''

class FSMInfo(StatesGroup):
    name_telefon_client = State()
    question = State()

# Начало диалога перехода в машинное состояние
@dp.message_handler(commands = 'Информация', state = None)
async def info_start(message : types.Message):
    await FSMInfo.name_telefon_client.set()
    await message.reply('Для уточнения информации по оформленному заказу ответьте на 2 вопроса.\n'
                       '\n1. Напишите номер телефона который был указан в заказе:', reply_markup=DELKB)

# Ловим первый ответ и загружаем в словарь
@dp.message_handler(state = FSMInfo.name_telefon_client)
async def load_name_telefon_client(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Телефон'] = message.text
    await FSMInfo.next()
    await message.reply('Информация принята! \n\n2. Теперь напишите Ваш вопрос по заказу:')

# Ловим последний ответ
@dp.message_handler(state = FSMInfo.question)
async def load_question(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['Вопрос'] = message.text
    await message.reply('Информация принят и передана менеджеру, он свяжется с Вами в ближайшее время!\nОстались вопросы - воспользуйтесь меню!', reply_markup=inclient_kb)
    async with state.proxy() as data:
        await bot.send_message(chat_id=ID_ADMIN_ECHO,text=(message.from_user.full_name, message.from_user.id, str(data)))
    await state.finish()

'''*********************** Ловим все входящие и даем ответ *********************'''

@dp.message_handler()
async def operator_work_command(message : types.Message):
    if message.text == '🟢 Оформить заказ':
        await cm_start(message)
    elif message.text == '❓ Информация по оформленному заказу':
        await info_start(message)
    elif message.text == '⏱ График работы':
        await bot.send_message(message.from_user.id,'Заказы через сайт Eco-List.ru принимаем кругласуточно, оператор отвечает: Пн-Пт с 12:00 до 20:00; Сб с 12:00 до 18:00; Вс - выходной.')
        await bot.send_message(chat_id=ID_ADMIN_ECHO,text=message.text)
    elif message.text == '📩 Написать оператору':
        await bot.send_message(message.from_user.id, 'Что бы написать оператору перейдите по ссылке: https://telegram.me/Eco_List')
        await bot.send_message(chat_id=ID_ADMIN_ECHO,text=message.text)
    else:
        await bot.send_message(message.from_user.id, 'Бот не нашел ответ, воспользуйтесь меню ниже.', reply_markup=inclient_kb)
        await bot.send_message(chat_id = ID_ADMIN_ECHO, text=(message.from_user.full_name, message.from_user.id, message.text))

'''********************************* Конец основного кода ********************'''



#bot.polling(none_stop=True, interval=0)
executor.start_polling(dp, skip_updates=True)
# executor.start_webhook(
    # dispatcher = dp,
    # webhook_path = '',
    # on_startup = on_startup,
    # on_shutdown = on_shutdown,
    # skip_updates = True,
    # host = '0.0.0.0',
    # port = int(os.environ.get('PORT', 5000)))
