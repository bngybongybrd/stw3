import sqlite3
import bcrypt
from flask import url_for, flash, redirect, request

def login_check(email_input, pw_input):
    #email_input = request.form.get['email'] # change the name of the '' field
    #pw_input = request.form.get['password'].encode('utf-08') # change the name of the '' field

    # Connect to database
    conn = sqlite3.connect('data.db') 
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password BLOB)''')
    c.execute('''SELECT * FROM users WHERE email = (?)''', (email_input,))

    # Assumes that the email is unique
    row = c.fetchall()
    conn.commit()
    c.close()
    if len(row) == 0:
      return [False]
    if bcrypt.checkpw(pw_input, row[0][2]) and row[0][0] == email_input: # checks if the password matches the hashed password and if the email matches the email in the database
        #flash("Login successful", "success")  # password matches the hashed password
      a = [True, row[0][0], row[0][1]]
      #print(a[0])
      return a
      #redirect(url_for('real_home_page'))      # change the name of the '' field
    elif row[0][0] != email_input:
        #flash("Account does not exist", "warning")
        return [False]           # redirect(url_for('real_login')) # change the name of the '' field
    elif bcrypt.checkpw(pw_input, row[0][2]) == False:
        #flash("Incorrect password", "warning")
        return [False]        # redirect(url_for('real_login')) # change the name of the '' field

def sign_up(email_input, pw_input, username_input):
    #email_input = request.form.get['email'] # change the name of the '' field
    #pw_input = request.form.get['password'].encode('utf-08') # change the name of the '' field
    #username_input = request.form.get['username'] # change the name of the '' field
    
    # Connect to database
    conn = sqlite3.connect('data.db') 
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT, username TEXT, password BLOB)''')
    c.execute('''SELECT * FROM users WHERE email = ?''', (email_input,))

    row = c.fetchall()
    if row:
        #flash("Email already exists", "warning")
        return False #redirect(url_for('sign_up')) # change the name of the '' field
    else:
        hashed = bcrypt.hashpw(pw_input, bcrypt.gensalt())
        c.execute('''INSERT INTO users VALUES (?, ?, ?)''', (email_input, username_input, hashed))
        conn.commit()
        c.close()
        #flash("Sign up successful", "success")
        return True #redirect(url_for('login')) # change the name of the '' field

def insert_personal_info(email, age, gender, ch, bp, smoking):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personalinfo (email TEXT PRIMARY KEY, age TEXT, gender TEXT, ch TEXT, bp TEXT, smoking BOOLEAN)''')
    c.execute('''SELECT * FROM personalinfo WHERE email = (?)''', (email,))

    row = c.fetchall()
    if len(row) == 0:
      c.execute('''INSERT INTO personalinfo VALUES (?, ?, ?, ?, ?, ?)''', (email, age, gender, ch, bp, smoking))
    else:
      c.execute('''UPDATE personalinfo SET email=?, age=?, gender=?, ch=?, bp=?, smoking=? WHERE email=?''', (email, age, gender, ch, bp, smoking, email))

    conn.commit()
    c.close()

def get_personal_info(email):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personalinfo (email TEXT PRIMARY KEY, age TEXT, gender TEXT, ch TEXT, bp TEXT, smoking BOOLEAN)''')
    c.execute('''SELECT * FROM personalinfo WHERE email = (?)''', (email,))

    row = c.fetchall()
    return row