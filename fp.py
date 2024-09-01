import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import font
import time
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/Login")
root = None
image_item = None
canvas = None
image_data = None

def click():
    global image_data
    root.destroy()
    import main
    main.validate_login_biometric(image_data)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def login():
    root.destroy()
    import main
    main.load_ui()

def load_ui():
    global root, canvas
    root = tk.Tk()
    root.title("Bio-Metric Barrier System")
    root.geometry("601x501")
    root.configure(bg="#FFFFFF")

    canvas = tk.Canvas(
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
        outline=""
    )

    canvas.create_rectangle(
        4.0,
        4.0,
        596.0,
        496.0,
        fill="#080808",
        outline=""
    )

    canvas.create_rectangle(
        16.0,
        43.0,
        585.0,
        484.0,
        fill="#87ceeb",
        outline=""
    )

    canvas.create_text(
        189.0,
        58.0,
        anchor="nw",
        text="Select your fingerprint",
        fill="#000000",
        font=("Inter Bold", 24 * -1)
    )

    canvas.create_rectangle(
        58.0,
        110.0,
        539.0,
        450.0,
        fill="#87ceeb",
        outline=""
    )

    canvas.create_rectangle(
        16.0,
        10.0,
        83.0,
        37.0,
        fill="#FFFFFF",
        outline=""
    )

    canvas.create_text(
        25.0,
        16.0,
        anchor="nw",
        text="FP",
        fill="#000000",
        font=("Inter Bold",16 * -1)
    )

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

    canvas.create_rectangle(
        200,
        175,
        400,
        375,
        fill="#000000",
        outline="white",
        dash=(50, 20)
    )
    drag_box = canvas.create_text(
        255,
        260,
        anchor="nw",
        text="Click here to Scan\n or Load Image",
        fill="#FFFFFF",
        font=("Inter", 14 * -1)
    )

    canvas.tag_bind(drag_box, "<Button-1>", on_click)

    submit_image = PhotoImage(file=relative_to_assets("submit.png"))
    submit = Button(
        root,
        image=submit_image,
        borderwidth=0,
        highlightthickness=0,
        relief="raised",
        bd=3,
        command=click
    )
    root.bind('<Escape>', lambda e: login())
    submit.place(
        x=253.0,
        y=407.0,
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

    

def load_image():
    global image_item, image_data


    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    
    if not file_path:
        return
    else:
        with open(file_path, 'rb') as file:
            image_data = file.read()
        
        image = Image.open(file_path)
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)


        if image_item:
            canvas.delete(image_item)


        image_item = canvas.create_image(301.5, 275.5, image=tk_image)
        canvas.image = tk_image

def on_click(event):
    """Simulate dropping the image when the box is clicked."""
    x, y = event.x, event.y


    if 200 < x < 400 and 175 < y < 375:
        load_image()

if __name__ == "__main__":
    load_ui()