import mysql.connector as sql
conn = sql.connect(
    host="localhost",
    user="root",
    passwd="root@1234",
    database="AkBank",
    use_pure=True
)
cur = conn.cursor()
cur.execute("CREATE TABLE transactions(acc_no INT(11),date date, withdrawal_amt bigint(20), amount_added bigint(20))")