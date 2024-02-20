import mysql.connector as sql
conn = sql.connect(
    host="localhost",
    user="root",
    passwd="root@1234",
    database="AkBank",
    use_pure=True
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        acc_no INT(11),
        trans_date DATE,
        withdrawal_amt BIGINT(20),
        amount_added BIGINT(20)
    )
""")
