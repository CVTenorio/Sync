import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import sqlite3
import os
import re

# Ensure directories exist
os.makedirs("assets/database", exist_ok=True)
os.makedirs("assets/json", exist_ok=True)

DB_PATH = "assets/database/users.db"
JSON_PATH = "assets/json/users.json"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT UNIQUE,
                      middle_name TEXT,
                      last_name TEXT,
                      email TEXT UNIQUE,
                      birthday TEXT,
                      gender TEXT)''')
    conn.commit()
    conn.close()

setup_database()

def user_exists(first_name, last_name, email):
    try:
        with open(JSON_PATH, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    if any(user["first_name"] == first_name and user["last_name"] == last_name or user["email"] == email for user in users):
        return True
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ? OR email = ?", (first_name, last_name, email))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def save_data():
    first_name = entry_first_name.get()
    middle_name = entry_middle_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    birthday = entry_birthday.get_date().strftime('%Y-%m-%d')
    gender = ", ".join([g for g, var in gender_vars.items() if var.get()])
    
    if not first_name or not middle_name or not last_name or not email or not birthday or not gender:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return
    
    if len(middle_name) < 3 or len(middle_name) > 50:
        messagebox.showerror("Error", "Middle name must be between 3 and 50 characters.")
        return
    
    if first_name == middle_name or first_name == last_name or middle_name == last_name:
        messagebox.showerror("Error", "Fields cannot have the same value.")
        return
        
    
    if user_exists(first_name, last_name, email):
        messagebox.showerror("Error", "Oops! This user or email is already saved.")
        return
    
    user_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "email": email,
        "birthday": birthday,
        "gender": gender
    }
    
    try:
        with open(JSON_PATH, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    users.append(user_data)
    with open(JSON_PATH, "w+") as file:
        json.dump(users, file, indent=4)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (first_name, middle_name, last_name, email, birthday, gender) VALUES (?, ?, ?, ?, ?, ?)",
                   (first_name, middle_name, last_name, email, birthday, gender))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "User registered successfully!")
    signup_window.grab_release()
    signup_window.destroy()
    root.deiconify()

def clear_fields():
    entry_first_name.delete(0, tk.END)
    entry_middle_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_birthday.set_date('')
    for var in gender_vars.values():
        var.set(0)

def on_closing():
    root.quit()

def open_signup():
    global signup_window, gender_vars
    root.withdraw()
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign-Up Form")
    signup_window.geometry("450x500")
    signup_window.configure(bg="#2C2C2C")
    signup_window.grab_set()
    signup_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    tk.Label(signup_window, text="First Name:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    global entry_first_name
    entry_first_name = tk.Entry(signup_window, font=("Arial", 12))
    entry_first_name.pack()
    
    tk.Label(signup_window, text="Middle Name:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    global entry_middle_name
    entry_middle_name = tk.Entry(signup_window, font=("Arial", 12))
    entry_middle_name.pack()
    
    tk.Label(signup_window, text="Last Name:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    global entry_last_name
    entry_last_name = tk.Entry(signup_window, font=("Arial", 12))
    entry_last_name.pack()
    
    tk.Label(signup_window, text="Email:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    global entry_email
    entry_email = tk.Entry(signup_window, font=("Arial", 12))
    entry_email.pack()
    
    tk.Label(signup_window, text="Birthday:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    global entry_birthday
    entry_birthday = DateEntry(signup_window, date_pattern='yyyy-MM-dd', background='black', foreground='yellow', borderwidth=2)
    entry_birthday.pack()
    
    tk.Label(signup_window, text="Gender:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    gender_vars = {gender: tk.IntVar() for gender in ["Male", "Female", "Other"]}
    for gender, var in gender_vars.items():
        tk.Checkbutton(signup_window, text=gender, variable=var, bg="#2C2C2C", fg="#FFD700", font=("Arial", 12, "bold"), selectcolor="#2C2C2C").pack()
    
    tk.Button(signup_window, text="Register", command=save_data, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Button(signup_window, text="Clear", command=clear_fields, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack()
    tk.Button(signup_window, text="Back", command=go_back, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(pady=5)

def go_back():
    signup_window.grab_release()
    signup_window.destroy()
    root.deiconify()
    
    tk.Button(signup_window, text="Back", command=go_back, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(pady=5)


#View all records
#database and json file 
def view_all_records():
    records = []
    
    # Fetch records from the database
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, middle_name, last_name, birthday, gender FROM users")
        db_records = cursor.fetchall()
        conn.close()
        
        for record in db_records:
            records.append({
                "first_name": record[0],
                "middle_name": record[0],
                "last_name": record[0],
                "email": record[0],
                "birthday": record[0],
                "gender": record[0]
            })
    
    # Fetch records from the JSON file
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r") as file:
                json_records = json.load(file)
                if isinstance(json_records, list):
                    records.extend(json_records)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    return records

# Example usage:
all_users = view_all_records()
print(all_users)



root = tk.Tk()
root.title("Sync")
root.geometry("300x200")
root.configure(bg="#2C2C2C")
root.protocol("WM_DELETE_WINDOW", on_closing)

tk.Button(root, text="Sign Up", command=open_signup, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(expand=True)

root.mainloop()
