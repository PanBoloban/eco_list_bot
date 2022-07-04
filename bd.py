import pymysql
from constant import HOST, USER_LOG_HOST, PASSW_HOST, NAME_BD

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
        with connection.cursor() as cursor:
            # select_order = "SELECT id AS nomer, state_id AS status FROM `shop_order` ORDER BY id DESC LIMIT 500"
            select_order = "SELECT contact_id, field, value FROM `wa_contact_data` WHERE field = 'phone'"
            cursor.execute(select_order)
            rows = cursor.fetchall()
            # print(rows[1])
            # list = []
            # for row in rows:
                # for value in row.values():
                    # list.append(value)
            # dictionary = dict(zip(list[0:1000:2], list[1:1000:2]))



    finally:
        connection.close()

except Exception as ex:
    print('Connection refused...')
    print(ex)
