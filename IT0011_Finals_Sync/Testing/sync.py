print("Hi pre!")

'''
This is a test file for the sync.py script.
'''
'''
Testing Login 
Suggestion: 
1st panel = Sign up -> Sign In
2nd panel = 
'''
from tkinter import *
import customtkinter


window = Tk()
window.title("Account_SignUp")
window.geometry("350x350")
window.configure(bg="#FFFFFF")


Label_id5 = customtkinter.CTkLabel(
    master=window,
    text="WELCOME TO SYNC",
    font=("Arial", 16),
    text_color="#000000",
    height=30,
    width=150,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id5.place(x=100, y=130)
Button_id7 = customtkinter.CTkButton(
    master=window,
    text="Sign-In",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=95,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id7.place(x=180, y=170)
Button_id6 = customtkinter.CTkButton(
    master=window,
    text="Sign-Up",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=95,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id6.place(x=80, y=170)

window.mainloop()