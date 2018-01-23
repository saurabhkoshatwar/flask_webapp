import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def dbtest(id):
	cur = conn.cursor()
	cur.execute('SELECT name from test WHERE id='+str(id))
	rows = cur.fetchall()
	print(rows)
	for row in rows:
		return row[0]

def email_already_exists(email):
	cur = conn.cursor()
	cur.execute("SELECT * from s_details WHERE email=+\'%s\'", (email))
	if cur.rowcount<=0:
		return False