import pymysql
from constant import HOST, USER_LOG_HOST, PASSW_HOST, NAME_BD


def connect_bd_nomber():
    try:
        connection = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER_LOG_HOST,
            password=PASSW_HOST,
            database=NAME_BD,
            cursorclass=pymysql.cursors.DictCursor
        )
    
        try:
            '''***********  Выборка по номеру заказа  ***********'''
            with connection.cursor() as cursor:
                select_order = "SELECT id AS nomer, state_id AS status FROM `shop_order` ORDER BY id DESC LIMIT 500"
                cursor.execute(select_order)
                rows = cursor.fetchall()
                list_order = []
                for row in rows:
                    # print(row)
                    for value in row.values():
                        list_order.append(value)
                dict_order = dict(zip(list_order [0:1000:2], list_order [1:1000:2])) # словарь заказ: статус; усли по номеру заказа то ставим лимит 1000
                
                # print(dict_order)
                # print(list)
    
        finally:
            connection.close()
    
    except Exception as ex:
        print('Connection refused...')
        print(ex)
    return dict_order

def connect_bd_phon_st():
    try:
        connection = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER_LOG_HOST,
            password=PASSW_HOST,
            database=NAME_BD,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            '''************* Выборка телефон=статус  *************'''
            with connection.cursor() as cursor:
                select_status = "SELECT wa_contact_data.value, shop_order.state_id FROM `shop_order`, `wa_contact_data` WHERE wa_contact_data.field = 'phone' AND wa_contact_data.contact_id = shop_order.contact_id"
                cursor.execute(select_status)
                rows2 = cursor.fetchall()
                # print(rows[1])
                list_status = []
                for row2 in rows2:
                    # print(row)
                    for value in row2.values():
                        list_status.append(value)
                dict_status = dict(zip(list_status[0::2], list_status[1::2])) # словарь телефон : статус
                # print(dict_status)
                # print(list)
    
        finally:
            connection.close()
    
    except Exception as ex:
        print('Connection refused...')
        print(ex)
    return dict_status

def connect_bd_phone_nam():
    try:
        connection = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER_LOG_HOST,
            password=PASSW_HOST,
            database=NAME_BD,
            cursorclass=pymysql.cursors.DictCursor
        )
    
        try:
            '''***************  Выборка телефон = номер заказа ***********'''
            with connection.cursor() as cursor:
                select_phone = "SELECT wa_contact_data.value, shop_order.id FROM `shop_order`, `wa_contact_data` WHERE wa_contact_data.field = 'phone' AND wa_contact_data.contact_id = shop_order.contact_id"
                cursor.execute(select_phone)
                rows3 = cursor.fetchall()
                # print(rows[1])
                list_phone = []
                for row3 in rows3:
                    # print(row)
                    for value in row3.values():
                        list_phone.append(value)
                dict_phone = dict(zip(list_phone[0::2], list_phone[1::2])) # словарь телефон: номер заказа
                # print(dict_phone)
                # print(list)
    
        finally:
            connection.close()
    
    except Exception as ex:
        print('Connection refused...')
        print(ex)
    return dict_phone
