import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
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
                      birthday TEXT,
                      gender TEXT)''')
    conn.commit()
    conn.close()

setup_database()

def user_exists(first_name, last_name):
    try:
        with open(JSON_PATH, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    if any(user["first_name"] == first_name and user["last_name"] == last_name for user in users):
        return True
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ?", (first_name, last_name))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def save_data():
    first_name = entry_first_name.get()
    middle_name = entry_middle_name.get()
    last_name = entry_last_name.get()
    birthday = entry_birthday.get_date().strftime('%Y-%m-%d')
    gender = ", ".join([g for g, var in gender_vars.items() if var.get()])
    
    if not first_name or not middle_name or not last_name or not birthday or not gender:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return
    
    if len(middle_name) < 3 or len(middle_name) > 50:
        messagebox.showerror("Error", "Middle name must be between 3 and 50 characters.")
        return
    
    if first_name == middle_name or first_name == last_name or middle_name == last_name:
        messagebox.showerror("Error", "Fields cannot have the same value.")
        return
        
    if user_exists(first_name, last_name):
        messagebox.showerror("Error", "Oops! This user is already saved.")
        return
    
    user_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
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
    cursor.execute("INSERT INTO users (first_name, middle_name, last_name, birthday, gender) VALUES (?, ?, ?, ?, ?)",
                   (first_name, middle_name, last_name, birthday, gender))
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
    entry_birthday.set_date('')

    for var in gender_vars.values():
        var.set(0)

def on_closing():
    root.quit()

def open_signup():
    global signup_window, gender_vars, image_label, image
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

def view_all_records():
    global view_window, search_entry, ViewRecords
    root.withdraw()
    view_window = tk.Toplevel(root)
    view_window.title("All User Records")
    view_window.geometry("600x450")
    view_window.configure(bg="#2C2C2C")
    view_window.grab_set()
    view_window.protocol("WM_DELETE_WINDOW", close_view_window)
    
    tk.Label(view_window, text="Search by First Name:", bg="#2C2C2C", fg="#FFD700", font=("Arial", 10, "bold")).pack()
    search_entry = tk.Entry(view_window, font=("Arial", 12))
    search_entry.pack()
    tk.Button(view_window, text="Search", command=search_records, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(pady=5)
    
    ViewRecords = ttk.Treeview(view_window, columns=("First Name", "Middle Name", "Last Name", "Birthday", "Gender"), show="headings")
    
    for col in ["First Name", "Middle Name", "Last Name", "Birthday", "Gender"]:
        ViewRecords.heading(col, text=col)
        ViewRecords.column(col, width=120)
    
    ViewRecords.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    tk.Button(view_window, text="Back", command=close_view_window, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(pady=5)
    
    load_records()

def load_records(filter_name=None):
    ViewRecords.delete(*ViewRecords.get_children())  # Clear any existing data in the table
    records = []
    existing_names = set()

    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = """SELECT first_name, middle_name, last_name, birthday, gender FROM users"""
        params = ()
        
        if filter_name:
            # Update query to search by first name, middle name, or last name
            query += """ WHERE first_name LIKE ? OR middle_name LIKE ? OR last_name LIKE ?"""
            params = (f"%{filter_name}%", f"%{filter_name}%", f"%{filter_name}%")
        
        cursor.execute(query, params)
        db_records = cursor.fetchall()
        conn.close()

        for record in db_records:
            name_tuple = (record[0], record[2])
            if name_tuple not in existing_names:
                existing_names.add(name_tuple)
                records.append(record)
                
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r") as file:
                json_records = json.load(file)
                if isinstance(json_records, list):
                    for record in json_records:
                        name_tuple = (record["first_name"], record["last_name"])
                        if name_tuple not in existing_names:
                            existing_names.add(name_tuple)
                            if not filter_name or (filter_name.lower() in record["first_name"].lower() or
                                                    filter_name.lower() in record["middle_name"].lower() or
                                                    filter_name.lower() in record["last_name"].lower()):
                                records.append((
                                    record["first_name"],
                                    record["middle_name"],
                                    record["last_name"],
                                    record["birthday"],
                                    record["gender"]
                                ))
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    for record in records:
        ViewRecords.insert("", tk.END, values=record)

def search_records():
    filter_name = search_entry.get().strip()
    if filter_name:
        load_records(filter_name)  # Load records based on the filter_name
    else:
        # If the search box is empty, clear the displayed records
        ViewRecords.delete(*ViewRecords.get_children())

def close_view_window():
    view_window.grab_release()
    view_window.destroy()
    root.deiconify()

def clear_all_data():
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all records? This action cannot be undone.")
    
    if confirmation:
        # Clear JSON file
        try:
            with open(JSON_PATH, "w") as file:
                json.dump([], file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear JSON file: {e}")
            return

        # Clear SQLite database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")  # Delete all records
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear database: {e}")
            return

        messagebox.showinfo("Success", "All records have been cleared!")
        load_records()


root = tk.Tk()
root.title("Sync")
root.geometry("300x200")
root.configure(bg="#2C2C2C")
root.protocol("WM_DELETE_WINDOW", on_closing)

 #image here testing


tk.Button(root, text="Sign Up", command=open_signup, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(expand=True)
tk.Button(root, text="View Records", command=view_all_records, bg="black", fg="#FFD700", font=("Arial", 12, "bold")).pack(expand=True)

root.mainloop()
