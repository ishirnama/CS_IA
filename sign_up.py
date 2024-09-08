from pathlib import Path
import emoji
import random
from datetime import datetime
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from tkinter import messagebox
import database
import io
import scanner
import re

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/Signup")
root = None 
forename = None 
surname = None 
dob = None 
email = None 
username=None 
password = None
rng_pwd = None
image_item = None
canvas = None
image_data = None

def back_to_login():
    root.destroy()
    import main
    main.load_ui()

def password_checker(password):
    flag = 0
    if (len(password)<=6):
        flag = -1
        print("length")
    elif not re.search("[a-z]", password):
        flag = -1
        print("small")
    elif not re.search("[A-Z]", password):
        flag = -1
        print("cap")
    elif not re.search("[0-9]", password):
        flag = -1
        print("num")
    else:
        flag = 0
    
    return flag
def submit_clicked():
    if forename.get() != "" and surname.get() != "" and dob.get != "" and email.get() != "" and username.get() != "" and password.get() != "" and image_data != None and password_checker(password.get())==0:
        
        print("user")
        img1 = Image.open(io.BytesIO(image_data))
        img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
        if database.find_user_by_username(username.get()) == None and scanner.match_in_db(img1) == None:
            database.insert_user( username.get(), password.get(), email.get(), forename.get(), surname.get(),age= calc_age(dob.get()), fingerprint=image_data,
            dob=dob.get(), pixelsum=scanner.get_pixel_sum(image_data), join_date=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            messagebox.showinfo("Success", f"{username.get()} signedup. Please login with username/password or fingerprint")
            back_to_login()
        else:
            messagebox.showinfo("Error", "Invalid user. Either fingerprint or user already exists")
    elif password.get() != "" and password_checker(password.get())!=0:
        messagebox.showinfo("Error", "Password should be atleast length of 6 with one small, one capital and one number charecter")
    else:
        print("datetime.now(): "+datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        messagebox.showinfo("Error", "All fields are mandatory")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def clear_fields(field):
    field.delete(0, 'end')


def clear_placeholder(event):
    if (dob.get() == "D D / M M / Y Y Y Y"):
        dob.delete(0, 'end')
        dob.config(fg="#000716")


def restore_placeholder(event):
    if dob.get() == "":
        dob.insert(0, "D D / M M / Y Y Y Y")
        dob.config(fg='grey')


def on_type(event):
    if dob.get() != "D D / M M / Y Y Y Y" and dob.cget('fg') == 'grey':
        dob.config(fg="#000716")


def calc_age(st_dob):
    x = st_dob.split("/")
    year_of_birth = int(x[2])
    curr_year = datetime.now().year
    age = curr_year - year_of_birth
    return age


def generate():
    print("rand passwd clicked ")
    clear_fields(rng_pwd)
    pwd = ""
    int = random.randint(0, 1000)
    for i in range(0, 5):
        instring = chr(random.randint(97, 122))
        pwd = f"{pwd}{instring}"
    fpwd = f"{pwd}{instring}{int}"
    print("rand passwd: "+fpwd)
    rng_pwd.insert(0, fpwd)


def load_ui():
    global root, forename, surname, dob, email, username, password, rng_pwd, canvas
    root = Tk()
    root.title("Bio-Metric Barrier System")
    button_hit_count = 0
    root.geometry("601x501")
    root.configure(bg = "#FFFFFF")
    root.bind('<Escape>', lambda e : back_to_login())


    canvas = Canvas(
        root,
        bg = "#FFFFFF",
        height = 501,
        width = 601,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    submit_img = PhotoImage(
        file=relative_to_assets("submit.png"))
    submit = Button(
        image=submit_img,
        borderwidth=0,
        highlightthickness=0,
        command=submit_clicked,
        relief="raised",
        bd=3,
    )
    submit.place(
        x=207.0,
        y=441.0,
        width=82.96632385253906,
        height=25.889514923095703
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        601.0,
        501.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        5.0,
        4.0,
        597.0,
        496.0,
        fill="#080808",
        outline="")

    canvas.create_rectangle(
        17.0,
        10.0,
        110.0,
        37.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        35.0,
        15.0,
        anchor="nw",
        text="Sign Up",
        fill="#000000",
        font=("Inter Bold", 16 * -1)
    )

    exit_img = PhotoImage(
        file=relative_to_assets("exit.png"))
    exit = Button(
        image=exit_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: back_to_login(),
        relief="raised"
    )
    exit.place(
        x=548.0,
        y=11.0,
        width=37.825157165527344,
        height=23.4222412109375
    )

    canvas.create_rectangle(
        17.0,
        45.0,
        586.0,
        487.0,
        fill="#87ceeb",
        outline="")

    canvas.create_rectangle(
        320.65208556056643,
        43.99786376953125,
        322.2838134765625,
        496.0018318250641,
        fill="#000000",
        outline="")

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    forename_img = canvas.create_image(
        170.5,
        103.0,
        image=entry_image_5
    )
    forename = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    forename.config(font=("Courier", 14))
    forename.place(
        x=32.0,
        y=82.0,
        width=277.0,
        height=40.0
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    username_img = canvas.create_image(
        455.0,
        103.0,
        image=entry_image_6
    )
    username = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    username.config(font=("Courier", 14))
    username.place(
        x=335.0,
        y=82.0,
        width=240.0,
        height=40.0
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    rng_pwd_field = canvas.create_image(
        455.0,
        393.0,
        image=entry_image_7
    )
    rng_pwd = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    rng_pwd.config(font=("Courier", 14))
    rng_pwd.place(
        x=335.0,
        y=372.0,
        width=240.0,
        height=40.0
    )

    canvas.create_text(
        32.0,
        51.0,
        anchor="nw",
        text="Forename :",
        fill="#000000",
        font=("Courier", 14)
    )

    entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    email_img = canvas.create_image(
        170.5,
        372.0,
        image=entry_image_8
    )
    email = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    email.config(font=("Courier", 14))
    email.place(
        x=32.0,
        y=351.0,
        width=277.0,
        height=40.0
    )

    canvas.create_text(
        32.0,
        320.0,
        anchor="nw",
        text="Email :",
        fill="#000000",
        font=("Courier", 14)
    )

    entry_image_9 = PhotoImage(
        file=relative_to_assets("entry_9.png"))
    surname_img = canvas.create_image(
        170.5,
        183.0,
        image=entry_image_9
    )
    surname = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    surname.config(font=("Courier", 14))
    surname.place(
        x=32.0,
        y=162.0,
        width=277.0,
        height=40.0
    )

    canvas.create_text(
        32.0,
        131.0,
        anchor="nw",
        text="Surname :",
        fill="#000000",
        font=("Courier", 14)
    )

    dob = Entry(
        bd=5,
        bg="#F0FCFF",
        highlightthickness=0
    )
    dob.config(font=("Courier", 14), fg='grey')
    dob.insert(0, "D D / M M / Y Y Y Y")
    dob.bind("<FocusIn>", clear_placeholder)
    dob.bind("<FocusOut>", restore_placeholder)
    dob.bind("<Key>", on_type)
    dob.place(
        x=32.0,
        y=253.0,
        width=277.0,
        height=40.0
    )

    canvas.create_text(
        32.0,
        219.0,
        anchor="nw",
        text="Date of Birth :",
        fill="#000000",
        font=("Courier", 14)
    )

    canvas.create_text(
        339.0,
        51.0,
        anchor="nw",
        text="Pick a Username :",
        fill="#000000",
        font=("Courier", 14)
    )

    canvas.create_text(
        365.0,
        320.0,
        anchor="nw",
        text="Randomly Generate\n    Password",
        fill="#000000",
        font=("Courier", 14)
    )

    canvas.create_rectangle(
        321.0,
        312.0,
        593.0015241482979,
        313.4190888145754,
        fill="#000000",
        outline=""
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    roll = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=generate,
        relief="raised",
        bd=3
    )
    roll.place(
        x=407.0,
        y=441.0,
        width=93.0,
        height=32.0
    )

    entry_image_13 = PhotoImage(
        file=relative_to_assets("entry_13.png"))
    entry_bg_13 = canvas.create_image(
        455.0,
        198.0,
        image=entry_image_13
    )
    password = Entry(
        bd=5,
        bg="#F0FCFF",
        fg="#000716",
        highlightthickness=0
    )
    password.config(font=("Courier", 14))
    password.place(
        x=335.0,
        y=177.0,
        width=240.0,
        height=40.0
    )

    canvas.create_text(
        339.0,
        147.0,
        anchor="nw",
        text="Pick a Password :",
        fill="#000000",
        font=("Courier", 14)
    )

    canvas.create_rectangle(
        330,
        225,
        573,
        310,
        fill="#000000",
        outline="white",
        dash=(50, 20)
    )
    drag_box = canvas.create_text(
        360,
        250,
        anchor="nw",
        text="Click here to \nScan or Load \nFingerprint",
        fill="#FFFFFF",
        font=("Inter", 14 * -1)
    )

    canvas.tag_bind(drag_box, "<Button-1>", load_image)

    root.resizable(False, False)
    window_height = 501
    window_width = 601

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    root.mainloop()

def load_image(event=None):

    print("load_image clicked: ")
    global image_item, image_data


    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    
    if not file_path:
        return
    else:
        with open(file_path, 'rb') as file:
            image_data = file.read()
        
        image = Image.open(file_path)
        image = image.resize((90, 90), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)


        if image_item:
            canvas.delete(image_item)


        image_item = canvas.create_image(500.5, 270.5, image=tk_image)
        canvas.image = tk_image

if __name__ == "__main__":
    load_ui()