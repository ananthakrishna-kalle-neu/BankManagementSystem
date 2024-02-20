import mysql.connector as sql
conn = sql.connect(
    host="localhost",
    user="root",
    passwd="root@1234",
    database="AkBank",
    use_pure=True
)
cur = conn.cursor()
cur.execute("CREATE TABLE user_table (username varchar(25) PRIMARY KEY,password varchar(25) NOT NULL)")