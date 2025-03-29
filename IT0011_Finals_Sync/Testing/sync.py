print("Hi pre!")

'''
This is a test file for the sync.py script.
'''
'''
Testing Login Panel
'''
from tkinter import *
import customtkinter

def save_to_file():
    email = Entry_id2.get()
    password = Entry_id6.get()
    
    with open("admin_data.txt", "a") as file:  
        file.write(f"Email: {email}\nPassword: {password}\n\n")
    
    print("Data Saved Successfully!") 

window = Tk()
window.title("Welcome")
window.geometry("400x350")
window.configure(bg="#908989")

Entry_id6 = customtkinter.CTkEntry(
    master=window,
    placeholder_text="Password..",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=195,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#908989",
    fg_color="#F0F0F0",
)
Entry_id6.place(x=100, y=160)

Label_id3 = customtkinter.CTkLabel(
    master=window,
    text="Welcome To Sync",
    font=("Arial", 18),
    text_color="#000000",
    height=30,
    width=150,
    corner_radius=0,
    bg_color="#908989",
    fg_color="#ca7777",
)
Label_id3.place(x=120, y=20)

Entry_id2 = customtkinter.CTkEntry(
    master=window,
    placeholder_text="Email..",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=195,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#908989",
    fg_color="#F0F0F0",
)
Entry_id2.place(x=100, y=130)

Button_id4 = customtkinter.CTkButton(
    master=window,
    text="SUBMIT",
    font=("Arial", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=95,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#908989",
    fg_color="#F0F0F0",
    command=save_to_file  
)
Button_id4.place(x=140, y=210)

Label_id5 = customtkinter.CTkLabel(
    master=window,
    text="Login",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#908989",
    fg_color="#908989",
)
Label_id5.place(x=100, y=100)


window.mainloop()


