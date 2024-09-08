
from pathlib import Path
import emoji
import tkinter as tk
from tkinter import *
from tkinter import font
import time
from datetime import datetime
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageFilter
import database
from tkinter import messagebox
import io
import scanner

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/Login")

ret_username = ""
ret_password = ""
count = 3
root = None
username = None
password = None

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def clear_fields(user, pwd):
    user.delete(0, END)
    pwd.delete(0, END)

def signup(event=None):
    clear_fields(username, password)
    root.destroy()
    import sign_up
    sign_up.load_ui()

def biometric_login(event=None):
    clear_fields(username, password)
    root.destroy()
    import fp
    fp.load_ui()

def login():
    ret_username = (username.get())
    ret_password = (password.get())
    correct_username = "18namaish"
    correct_password = "ishirdgs"
    if (ret_username == correct_username) and (ret_password == correct_password):
        print("Signed in sucessfully")
        clear_fields(username, password)
        root.destroy()
        import menu
        user_record = database.find_user_by_username(ret_username)
        menu.load_ui(user_record)
    else:
        # print(round(time.time() * 1000))
        user_record = database.find_user_by_username(ret_username)
        if user_record is None:
            messagebox.showinfo("Error", "User not valid")
            clear_fields(username, password)
        elif user_record is not None and user_record[1] != ret_password and user_record[16]<2:
            messagebox.showinfo("Error", "User not valid")
            clear_fields(username, password)
            user_record =  list(user_record)
            user_record[16]=user_record[16]+1
            database.update_user(user_record)
        elif user_record is not None and user_record[1] != ret_password and user_record[16]==2 and user_record[15]==0:
            messagebox.showinfo("Error", "User not valid")
            clear_fields(username, password)
            user_record =  list(user_record)
            user_record[15]=round(time.time() * 1000)
            database.update_user(user_record)
        elif user_record is not None and user_record[16]==2 and ((round(time.time() * 1000)-user_record[15])/1000)/60<15:
            messagebox.showinfo("Error", f"User Locked. Please retry after for {int(15-((round(time.time() * 1000)-user_record[15])/1000)/60)} minutes")
            clear_fields(username, password)
        elif user_record is not None and user_record[1] == ret_password:
            clear_fields(username, password)
            root.destroy()
            user_record =  list(user_record)
            user_record[15]=0
            user_record[16]=0
            database.update_user(user_record)
            import menu
            menu.load_ui(user_record)
        else:
            print(((round(time.time() * 1000)-user_record[15])/1000)/60)
            messagebox.showinfo("Error", "User not valid. Unknown Error")
            clear_fields(username, password)
        
def validate_login_biometric(image_data):
    img1 = Image.open(io.BytesIO(image_data))
    img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
    row = scanner.match_in_db(img1)
    if row != None:
        import menu
        menu.load_ui(row)
    else:
        messagebox.showinfo("Error", "User not valid")
        load_ui()
        # clear_fields(username, password)        

def load_ui():
    global username, password, root
    root = Tk()
    root.title("Bio-Metric Barrier System")
    root.geometry("601x501")
    root.configure(bg="#FFFFFF")

    canvas = Canvas(
        root,
        bg="#FFFFFF",
        height=501,
        width=601,
        bd=0,
        highlightthickness=0,
        relief="raised"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        601.0,
        501.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        4.0,
        4.0,
        596.0,
        496.0,
        fill="#080808",
        outline="")

    canvas.create_rectangle(
        16.0,
        43.0,
        585.0,
        484.0,
        fill="#87ceeb",
        outline="")

    canvas.create_text(
        126.0,
        58.0,
        anchor="nw",
        text="Welcome to Bio-Metric Barrier",
        fill="#000000",
        font=("Inter Bold", 24 * -1,"underline")
    )

    canvas.create_rectangle(
        58.0,
        110.0,
        539.0,
        450.0,
        fill="#87ceeb",
        outline="")

    username_field_image = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    username_field = canvas.create_image(
        254.5,
        188.0,
        image=username_field_image
    )
    username = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0,
    )
    username.config(font=("Courier", 14))
    username.place(
        x=116.0,
        y=167.0,
        width=277.0,
        height=40.0
    )

    password_field_image = PhotoImage(file=relative_to_assets("entry_2.png"))
    password_field = canvas.create_image(
        254.5,
        272.0,
        image=password_field_image
    )
    password = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0,
    )
    password.config(
        font=("Courier",14),
        show=emoji.emojize(":skull:")
    )

    password.place(
        x=116.0,
        y=251.0,
        width=277.0,
        height=40.0
    )
    canvas.create_text(
        116.0,
        131.0,
        anchor="nw",
        text="Enter Username :",
        fill="#080808",
        font=("Courier",16)
    )

    canvas.create_text(
        118.0,
        218.0,
        anchor="nw",
        text="Enter Password :",
        fill="#080808",
        font=("Courier", 16)
    )


    canvas.create_rectangle(
        16.0,
        10.0,
        83.0,
        37.0,
        fill="#87ceeb",
        outline="")

    exit_image = PhotoImage(
        file=relative_to_assets("exit.png"))
    exit = Button(
        image=exit_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: root.destroy(),
        relief="raised"
    )

    exit.place(
        x=548.0,
        y=11.0,
        width=37.825157165527344,
        height=23.4222412109375
    )

    canvas.create_text(
        25.0,
        16.0,
        anchor="nw",
        text="Login",
        fill="#000000",
        font=("Inter Bold", 16 * -1)
    )

    submit = Button(root, command=login, text="Submit", font=(
                "Courier", 16), bd=3, relief=RIDGE, fg="#080808", anchor="nw")
    root.bind('<Escape>', lambda e: clear_fields(username, password))
    submit.place(
        x=113.0,
        y=307.0,
        width=82.96632385253906,
        height=25.889514923095703
    )
    bl = Button(root, command=biometric_login, text="Biometric Login", font=(
                "Courier", 16), bd=3, relief=RIDGE, fg="#080808", anchor="nw")
    bl.place(
        x=113.0,
        y=347.0,
        width=152.96632385253906,
        height=25.889514923095703
    )

    snp = Button(root, command=signup, text="Signup", font=(
                "Courier", 16), bd=3, relief=RIDGE, fg="#080808", anchor="nw")
    snp.place(
        x=113.0,
        y=387.0,
        width=82.96632385253906,
        height=25.889514923095703
    )

    root.resizable(False, False)
    window_height = 501
    window_width = 601

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    root.mainloop()

if __name__ == "__main__":
    load_ui()