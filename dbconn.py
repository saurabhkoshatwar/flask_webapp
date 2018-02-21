import os, string, random, datetime
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )


def dbtest(id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute('SELECT name from test WHERE id=' + str(id))
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        return row[0]
    conn.close()


def email_already_exists(email):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT email from s_details WHERE email='{0}'".format(email))
    print(cur.rowcount)
    to_return = False
    if cur.rowcount > 0:
        to_return = True
    conn.close()
    return to_return


def sign_up(name, email, password):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    api_key = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(7))
    try:
        cur.execute("INSERT INTO s_details (name, email, pass, api_key) VALUES ('{0}','{1}','{2}','{3}')".format(name, email, password, api_key))
        conn.commit()
        print('Inserted!')
    except:
        api_key = None
    conn.close()
    return api_key


def login(email, hashed_password):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    api_key = None
    cur = conn.cursor()
    cur.execute("SELECT api_key from s_details WHERE email='{0}' AND pass='{1}'".format(email, hashed_password))
    if cur.rowcount == 1:
        row = cur.fetchone()
        print(row[0])
        api_key=row[0]
        conn.close()

    return api_key


def get_tt(date, shift, batch):
    week = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY',
            'THURSDAY', 'FRIDAY', 'SATURDAY']
    weekday_num = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    weekday = week[(weekday_num+1)%7]
    #print(weekday)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT id, start_time, end_time, subject, teacher, room from time_table WHERE day ='{0}' AND shift='{1}' AND (batch='{2}' OR batch='-') ORDER BY id".format(weekday, shift, batch))
    regular_tt = cur.fetchall()
    if not regular_tt:
        return list(), 0
    print("yo +++++++++++++>>>>>>>>> \n", regular_tt)
    ids_to_check = tuple()
    for row in regular_tt:
        ids_to_check = ids_to_check+(row[0], )

    cur.execute("SELECT id_ptr, subject, teacher, room from changes WHERE chg_date ='{0}' AND id_ptr IN {1} ORDER BY id".format(
            date, ids_to_check))
    changes = cur.fetchall()
    conn.close()

    final_list = list()
    for reg_row in regular_tt:
        to_switch = False
        for changed_row in changes:
            if reg_row[0] == changed_row[0]:
                to_switch = True
                break
        if to_switch:
            j = {"Start Time": str(reg_row[1])[:5], "End Time": str(reg_row[2])[:5], "Subject": changed_row[1],
                            "Teacher": changed_row[2], "Room": changed_row[3], "Changed":1}
            final_list.append(j)
        else:
            j = {"Start Time": str(reg_row[1])[:5], "End Time": str(reg_row[2])[:5],
                            "Subject": reg_row[3], "Teacher": reg_row[4], "Room": reg_row[5], "Changed":0}
            final_list.append(j)

    print(final_list)
    return final_list, 1


def forgot(email, password):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        cur.execute("UPDATE s_details set pass='{0}' where email='{1}'".format(password, email))
        conn.commit()
        status = "password Updated"
    except:
        status = "password updating failed"
    conn.close()
    return status


def get_id_ptr(shift, day, start_time, batch):

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        #SELECT id_ptr from time_table WHERE  start_time='10:30:00' AND day='MONDAY' AND shift='I' AND batch='C'
        cur.execute("SELECT id from time_table WHERE  start_time='{0}' AND day='{1}' AND shift='{2}' AND batch='{3}'".format(start_time, day, shift, batch))
        id_ptr = cur.fetchall()

        status = "password Updated"
        conn.close()
        return id_ptr[0][0]
    except:
        status = "failed"
    conn.close()
    return -1


def find_previous_change(id_ptr,date):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        # SELECT * from changes WHERE  chg_date='2018-01-29' AND id_ptr='3'
        # print("insdide")
        cur.execute("SELECT * from changes WHERE  chg_date='{0}' AND id_ptr='{1}'".format(date, id_ptr))
        previous_change = cur.fetchall()
        conn.close()
        return list(previous_change)
    except:
        print("failed in db_query")
    conn.close()
    return -1


def delete_previous_change(delete_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        # delete from changes where id='1';
        cur.execute("delete from changes where id='{0}'".format(delete_id))
        conn.commit()
        conn.close()
        return ("Success")
    except:
        print("failed in deletion")
    conn.close()
    return -1


def insert_new_change(id_ptr, chg_date, subject, teacher, room):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        # INSERT INTO changes (id_ptr, chg_date, subject, teacher, room) VALUES ('7','201-9-12','blah','blurp','555')
        cur.execute("INSERT INTO changes (id_ptr, chg_date, subject, teacher, room) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(id_ptr, chg_date, subject, teacher, room))
        conn.commit()
        print('Inserted!')
        return "ok"
    except:
        api_key = None
    conn.close()
    return -1

def t_login(api_key):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    name = None
    cur = conn.cursor()
    cur.execute("SELECT name from t_details WHERE api_key='{0}'".format(api_key))
    if cur.rowcount == 1:
        row = cur.fetchone()
        print(row[0])
        name=row[0]
        conn.close()

    return name


def login_teacher(email, hashed_password):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    api_key = None
    cur = conn.cursor()
    cur.execute("SELECT api_key from teacher_details WHERE email='{0}' AND pass='{1}'".format(email, hashed_password))
    if cur.rowcount == 1:
        row = cur.fetchone()
        print(row[0])
        api_key=row[0]
        conn.close()

    return api_key


def email_already_exists_teacher(email):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT email from teacher_details WHERE email='{0}'".format(email))
    print(cur.rowcount)
    to_return = False
    if cur.rowcount > 0:
        to_return = True
    conn.close()
    return to_return
