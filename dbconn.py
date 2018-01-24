import os, string, random
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


def get_tt(day, shift, batch):
    weekday_num = datetime.strptime(date, '%Y-%m-%d').weekday()
    print(weekday_num)
    weekday = week[weekday_num]
    print(weekday)
    pass
