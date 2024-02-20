import datetime as dt
import mysql.connector as sql

# Establish connection
conn = sql.connect(
    host="localhost",
    user="root",
    passwd="root@1234",
    database="AkBank",
    use_pure=True
)
cur = conn.cursor()

# Create customer_details table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_details (
        acc_no INT PRIMARY KEY,
        acc_name VARCHAR(100) NOT NULL,
        phone_no BIGINT(20),
        address VARCHAR(255),
        cr_amt FLOAT NOT NULL DEFAULT 0.0
    )
""")

# Create transactions table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        acc_no INT(11),
        trans_date DATE,
        withdrawal_amt BIGINT(20),
        amount_added BIGINT(20)
    )
""")


conn.autocommit = True
c = 'y'

while c == 'y':
    print()
    print('1. CREATE BANK ACCOUNT')
    print('2. TRANSACTION')
    print('3. CUSTOMER DETAILS')
    print('4. TRANSACTION DETAILS')
    print('5. DELETE ACCOUNT')
    print('6. QUIT')
    print()
    n = int(input("Enter your CHOICE="))
    print()

    if n == 1:
        acc_no = int(input("Enter your ACCOUNT NUMBER= "))
        acc_name = input("Enter your ACCOUNT NAME= ")
        ph_no = int(input("Enter your PHONE NUMBER= "))
        address = input("Enter your current/permanent address= ")
        cr_amt = float(input("Enter your credit amount= "))

        V_SQLInsert = "INSERT INTO customer_details VALUES (%s, %s, %s, %s, %s)"
        data = (acc_no, acc_name, ph_no, address, cr_amt)
        cur.execute(V_SQLInsert, data)
        print("Account created successfully!!")

    elif n == 2:
        acc_no = int(input("Enter your account number= "))
        cur.execute("SELECT * FROM customer_details WHERE acc_no = %s", (acc_no,))
        data = cur.fetchall()
        count = cur.rowcount
        if count == 0:
            print("Account number Invalid. Please try again.")
        else:
            print("1. WITHDRAW AMOUNT")
            print("2. ADD AMOUNT")
            x = int(input("Enter your choice= "))
            if x == 1:
                amt = float(input("Enter withdrawal amount= "))
                cur.execute("SELECT cr_amt FROM customer_details WHERE acc_no = %s", (acc_no,))
                cr_amt = cur.fetchone()[0]
                if amt > cr_amt:
                    print("Insufficient balance")
                else:
                    cr_amt -= amt
                    cur.execute("UPDATE customer_details SET cr_amt = %s WHERE acc_no = %s", (cr_amt, acc_no))
                    cur.execute("INSERT INTO transactions (acc_no, trans_date, withdrawal_amt, amount_added) VALUES (%s, %s, %s, %s)", (acc_no, dt.datetime.today(), amt, 0))  # Assuming amount_added is 0 for withdrawals
                    print("Withdrawal Successful!")
            elif x == 2:
                amt = float(input("Enter amount to be added= "))
                cur.execute("SELECT cr_amt FROM customer_details WHERE acc_no = %s", (acc_no,))
                cr_amt = cur.fetchone()[0]
                cr_amt += amt
                cur.execute("UPDATE customer_details SET cr_amt = %s WHERE acc_no = %s", (cr_amt, acc_no))
                cur.execute("INSERT INTO transactions (acc_no, trans_date, withdrawal_amt, amount_added) VALUES (%s, %s, %s, %s)", (acc_no, dt.datetime.today(), 0, amt))  # Assuming withdrawal_amt is 0 for deposits
                print("Deposit Successful!")
            else:
                print("Invalid Choice!")

    elif n == 3:
        cur.execute("SELECT * FROM customer_details")
        data = cur.fetchall()
        print("Customer Details:")
        for row in data:
            print(row)

    elif n == 4:
        cur.execute("SELECT * FROM transactions")
        data = cur.fetchall()
        print("Transaction Details:")
        for row in data:
            print(row)

    elif n == 5:
        acc_no = int(input("Enter account number to delete= "))
        # First, delete the transactions related to the account
        cur.execute("DELETE FROM transactions WHERE acc_no = %s", (acc_no,))
        cur.execute("DELETE FROM customer_details WHERE acc_no = %s", (acc_no,))
        print("Account deleted successfully!")

    elif n == 6:
        quit()

    else:
        print("Invalid Choice! Thank you please visit again!")

# Close cursor and connection
cur.close()
conn.close()
