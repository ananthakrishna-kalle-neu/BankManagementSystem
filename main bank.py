import mysql.connector as sql

# Establish connection
conn = sql.connect(
    host="localhost",
    user="root",
    passwd="root@1234",
    database="AkBank",
    use_pure=True
)

# Create cursor
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_details (
        acct_no INT PRIMARY KEY,
        acct_name VARCHAR(25),
        phone_no BIGINT(25),
        address VARCHAR(25),
        cr_amt FLOAT
    )
""")

# Commit changes
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
