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

# Create user_table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password INT
    )
""")

print('====================================WELCOME TO AK BANK======================================')

import datetime as dt

print("1. REGISTER")
print("2. LOGIN")
print()

n = int(input("Enter your choice= "))
print()

if n == 1:
    name = input("Enter a Username: ")
    passwd = int(input("Enter a 4 DIGIT pin= "))
    
    # Insert user into user_table
    V_SQLInsert = "INSERT INTO user_table (password, username) VALUES (%s, %s)"
    data = (passwd, name)
    cur.execute(V_SQLInsert, data)
    conn.commit()
    
    print("USER created successfully")
    import menu

elif n == 2:
    name = input("Enter your Username= ")
    passwd = int(input("Enter your 4 DIGIT pin= "))
    
    # Check if username and password exist in user_table
    V_SQL_Sel = "SELECT * FROM user_table WHERE password = %s AND username = %s"
    data = (passwd, name)
    cur.execute(V_SQL_Sel, data)
    
    if cur.fetchone() is None:
        print("Invalid Username or Pin")
    else:
        print("Login successful")
        import menu
 
# Close cursor and connection
cur.close()
conn.close()
