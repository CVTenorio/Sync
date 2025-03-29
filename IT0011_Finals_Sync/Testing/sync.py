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
window.title("Sign Up Panel")
window.geometry("500x250")
window.configure(bg="#817e7e")

Signup_label = customtkinter.CTkLabel(
    master=window,
    text="Signup",
    font=("Times New Roman", 18),
    text_color="#000000",
    height=30,
    width=95,
    corner_radius=0,
    bg_color="#817e7e",
    fg_color="#817e7e",
)


window.mainloop()