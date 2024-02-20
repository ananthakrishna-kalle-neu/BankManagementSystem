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
        acct_no = int(input("Enter your account number= "))
        cur.execute("SELECT * FROM customer_details WHERE acct_no = %s", (acct_no,))
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
                cur.execute("SELECT cr_amt FROM customer_details WHERE acct_no = %s", (acct_no,))
                cr_amt = cur.fetchone()[0]
                if amt > cr_amt:
                    print("Insufficient balance")
                else:
                    cr_amt -= amt
                    cur.execute("UPDATE customer_details SET cr_amt = %s WHERE acct_no = %s", (cr_amt, acct_no))
                    cur.execute("INSERT INTO transactions (acct_no, trans_date, trans_type, trans_amt, cr_amt) VALUES (%s, %s, 'Withdrawal', %s, %s)", (acct_no, dt.datetime.today(), amt, cr_amt))
                    print("Withdrawal Successful!")
            elif x == 2:
                amt = float(input("Enter amount to be added= "))
                cur.execute("SELECT cr_amt FROM customer_details WHERE acct_no = %s", (acct_no,))
                cr_amt = cur.fetchone()[0]
                cr_amt += amt
                cur.execute("UPDATE customer_details SET cr_amt = %s WHERE acct_no = %s", (cr_amt, acct_no))
                cur.execute("INSERT INTO transactions (acct_no, trans_date, trans_type, trans_amt, cr_amt) VALUES (%s, %s, 'Deposit', %s, %s)", (acct_no, dt.datetime.today(), amt, cr_amt))
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
        cur.execute("DELETE FROM customer_details WHERE acct_no = %s", (acc_no,))
        print("Account deleted successfully!")

    elif n == 6:
        print('DO YOU WANT TO EXIT(y/n)')
        c = input("Enter your choice")

    else:
        print("Invalid Choice! Thank you please visit again!")
        quit()

# Close cursor and connection
cur.close()
conn.close()
