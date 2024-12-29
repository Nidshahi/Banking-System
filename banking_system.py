import sqlite3  #to interact with our db 
import re
import random
from datetime import datetime
connection = sqlite3.connect("banking_system.db")
cursor=connection.cursor() #allow to execute direct sql commands on db


cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    name TEXT, 
                    account_number TEXT PRIMARY KEY, 
                    dob TEXT, 
                    city TEXT, 
                    password TEXT, 
                    balance REAL, 
                    contact_number TEXT, 
                    email TEXT, 
                    address TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                    account_number TEXT PRIMARY KEY, 
                    password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    account_number TEXT, 
                    type TEXT, 
                    amount REAL, 
                    date TEXT)''')

def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def validate_password(p):
  if len(p)<6 :
    return False
  if not re.search("[A-Z]",p):
    return False
  if not re.search("[a-z]",p):
    return False
  if not re.search("[0-9]",p):
    return False
  return True

def addUser():
  name = input("Enter your name: ")
  account_number = generate_account_number()
  dob = input("Enter your date of birth (yyyy-mm-dd): ")
  city = input("Enter your city: ")

  while True:
      password = input("Enter a password (min 6 characters, 1 uppercase, 1 number): ")
      if validate_password(password):
          break
      print("Password does not meet the requirements.")

  balance = float(input("Enter the initial balance (min 2000): "))
  while balance < 2000:
        print("Initial balance must be at least 2000.")
        balance = float(input("Enter the initial balance: "))
 
  contact_number = input("Enter your contact number: ")
  email = input("Enter your email: ")
  address = input("Enter your address: ")
  cursor.execute("INSERT INTO users(name, account_number, dob, city, password, balance, contact_number, email, address) VALUES(?,?,?,?,?,?,?,?,?)",
                 (name, account_number, dob, city, password, balance, contact_number, email, address))
  cursor.execute("INSERT INTO login (account_number, password) VALUES (?, ?)", (account_number, password))
  connection.commit()#save chnages to db
  print(f"User added successfully! Your account number is {account_number}")

def show_user():
  account_number = input("Enter account number to display: ")
  cursor.execute("SELECT * FROM users WHERE account_number=?", (account_number,))
  user = cursor.fetchone()#retrieves a single row from the db
  if user:
    print("User Information:")
    print(f"Name: {user[0]}")
    print(f"Account Number: {user[1]}")
    print(f"DOB: {user[2]}")
    print(f"City: {user[3]}")
    print(f"Balance: {user[5]}")
    print(f"Contact: {user[6]}")
    print(f"Email: {user[7]}")
    print(f"Address: {user[8]}")
  else:
    print("User not found.")

def login():
  account_number = input("Enter your account number: ")
  password = input("Enter your password: ")
  cursor.execute("SELECT * FROM login WHERE account_number=? AND password=?", (account_number, password))
  user = cursor.fetchone()
  if user:
    print(f"Welcome, {account_number}!")
    user_menu(account_number)
  else:
    print("Invalid login credentials.")

def main():
    while True:
      print("\n1. Add User\n2. Show User\n3. Login\n4. Exit")
      choice = int(input("Enter your choice: "))
        
      if choice == 1:
        addUser()
      elif choice == 2:
        show_user()
      elif choice == 3:
        login()
      elif choice == 4:
        print("Exiting the system.")
        break
      else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    connection.close()