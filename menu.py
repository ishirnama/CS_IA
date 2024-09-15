
from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from scanner import Scanner
import io
import database

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/Menu")
image_item = None
root = None

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def back_to_login():
    root.destroy()
    import main
    main.load_ui()

def edit_details(user):
    root.destroy()
    import edit_details
    edit_details.load_ui(user)

def toggle_metadata(user):
    if user != None:
        if user[13] == 0:
            database.update_hide_metadata_by_username(user[0],1)
        elif user[13] == 1:
            database.update_hide_metadata_by_username(user[0],0)
        root.destroy()
        user = database.find_user_by_username(user[0])
        print(user[13])
        load_ui(user)

def toggle_userinformation(user):
    if user != None:
        if user[14] == 0:
            database.update_hide_userinformation_by_username(user[0],1)
        elif user[14] == 1:
            database.update_hide_userinformation_by_username(user[0],0)
        root.destroy()
        user = database.find_user_by_username(user[0])
        print(user[14])
        load_ui(user)

def toggle_theme(user):
    if user != None:
        if user[17] == "LIGHT":
            database.update_theme_by_username(user[0],"DARK")
        elif user[17] == "DARK":
            database.update_theme_by_username(user[0],"LIGHT")
        root.destroy()
        user = database.find_user_by_username(user[0])
        print(user[17])
        load_ui(user)

def load_ui(user_data):
    global image_item, root, user
    img = None
    text_background_color = "#000000"
    text_color = "#FFFFFF"
    if user_data != None:
        user = user_data
        img = Image.open(io.BytesIO(user_data[7]))
        if user_data[17] != None and user_data[17] == "LIGHT":
            text_background_color = "#FFFFFF"
            text_color = "#000000"

    root = Tk()
    root.title("Bio-Metric Barrier System")
    root.geometry("601x501")
    root.configure(bg = "#FFFFFF")


    canvas = Canvas(
        root,
        bg = "#FFFFFF",
        height = 501,
        width = 601,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
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
        4.0,
        4.0,
        596.0,
        496.0,
        fill="#080808",
        outline="")

    canvas.create_rectangle(
        14.0,
        44.0,
        586.0,
        485.0,
        fill="#87ceeb",
        outline="")

    canvas.create_rectangle(
        12.99998664855957,
        312.0064697265625,
        269.0000037541904,
        313.49286180679724,
        fill="#000000",
        outline="")
   
    canvas.create_rectangle(
        268.3487243652344,
        351.245273212312,
        586.0000187782498,
        353.196044921875,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        267.63430595979025,
        35.0,
        269.3480224609375,
        486.9971771864548,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        20.0,
        69.0,
        266.0,
        309.0,
        fill=text_background_color,
        outline="")
    
    canvas.create_text(
        20.0,
        49.0,
        anchor="nw",
        text="User Records",
        fill="#000000",
        font=("Courier", 14)
    )
    if user_data != None:
        user_records = database.find_user_records_by_username(user_data[0])
        count = 0
        for entry in user_records:
            canvas.create_text(
                20.0,
                80.0+count*30,
                anchor="nw",
                text=f"record_id: {entry[0]}",
                fill=text_color,
                font=("Courier", 14)
            )
            canvas.create_text(
                20.0,
                90.0+count*30,
                anchor="nw",
                text=f"visit_date: {entry[3]}",
                fill=text_color,
                font=("Courier", 14)
            )
            canvas.create_text(
                20.0,
                100.0+count*30,
                anchor="nw",
                text=f"purpose: {entry[2]}",
                fill=text_color,
                font=("Courier", 14)
            )
            count = count+1
    canvas.create_rectangle(
        488.0,
        362.0,
        579.0,
        479.0,
        fill="#87ceeb",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_userinformation(user_data),
        bd=3,
        relief="raised"
    )
    button_1.place(
        x=495.0,
        y=370.0,
        width=77.0,
        height=41.0
    )

    canvas.create_text(
        274.0,
        355.0,
        anchor="nw",
        text="Metadata ",
        fill="#000000",
        font=("Courier", 14)
    )

    exit_image = PhotoImage(
        file=relative_to_assets("exit.png"))
    exit = Button(
        image=exit_image,
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

    if user_data != None:
        if user_data[17] == "LIGHT":
            theme_image = PhotoImage(
                file=relative_to_assets("dark_theme.png"))
        else:
            theme_image = PhotoImage(
                file=relative_to_assets("light_theme.png"))
        theme = Button(
                image=theme_image,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: toggle_theme(user_data),
                relief="raised"
            )
        theme.place(
            x=498.0,
            y=11.0,
            width=37.825157165527344,
            height=23.4222412109375
        )

    edit_image = PhotoImage(
        file=relative_to_assets("edit.png"))
    edit = Button(
        image=edit_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: edit_details(user_data),
        relief="raised"
    )
    edit.place(
        x=428.0,
        y=11.0,
        width=57.825157165527344,
        height=23.4222412109375
    )

    canvas.create_rectangle(
        478.0,
        351.0,
        479.0,
        489.0,
        fill="#000000",
        outline="")
    canvas.create_rectangle(
        21.0,
        332.0,
        263.0,
        479.0,
        fill=text_background_color,
        outline="")

    canvas.create_text(
        20.0,
        314.0,
        anchor="nw",
        text="User Details",
        fill="#000000",
        font=("Courier", 14)
    )
    
    username = ""
    email=""
    forename=""
    surname=""
    age="" 
    dob=""
    join_date=""
    
    if user_data != None:
        if user_data[13] == 0:
            username = user_data[0]
            email = user_data[2]
            forename = user_data[3]
            surname = user_data[4]
            age = user_data[5]
            dob = user_data[8]
            join_date = user_data[10]
        else:
            username = "0x0x0x0x"
            email = "0x0x0x0x"
            forename = "0x0x0x0x"
            surname = "0x0x0x0x"
            age = "0x0x0x0x"
            dob = "0x0x0x0x"
            join_date = "0x0x0x0x"
        
    canvas.create_text(
        20.0,
        340.0,
        anchor="nw",
        text=f"username: {username}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        360.0,
        anchor="nw",
        text=f"forename: {forename}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        380.0,
        anchor="nw",
        text=f"surname : {surname}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        400.0,
        anchor="nw",
        text=f"age     : {age}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        420.0,
        anchor="nw",
        text=f"dob     : {dob}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        440.0,
        anchor="nw",
        text=f"join_date: {join_date}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_text(
        20.0,
        460.0,
        anchor="nw",
        text=f"email: {email}",
        fill=text_color,
        font=("Courier", 14)
    )
    canvas.create_rectangle(
        274.0,
        47.0,
        582.0,
        348.0,
        fill=text_background_color,
        outline="")

    if user_data != None:
        if user_data[14] == 0:
            img1 = img.resize((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(img1)
            if image_item:
                canvas.delete(image_item)
            image_item = canvas.create_image(424, 200.0, image=tk_image)
        else:
            scanner = Scanner()
            img1 = Image.fromarray(scanner.blur_image(user_data[7]))
            # img1 = img.resize((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(img1)
            if image_item:
                canvas.delete(image_item)
            image_item = canvas.create_image(424, 200.0, image=tk_image)


    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_metadata(user_data),
        relief="raised",
        bd=3
    )
    button_4.place(
        x=495.0,
        y=431.0,
        width=77.0,
        height=41.0
    )

    pixel_sum = ""
    width = "" 
    height = ""
    bit_depth = ""

    if user_data != None:
        if user_data[14] == 0:
            pixel_sum = user_data[9]
            width, height = img.size
            bit_depth = img.mode
        else:
            pixel_sum = "0x0x0x0x"
            width = "0x0x0x0x"
            height = "0x0x0x0x"
            bit_depth = "0x0x0x0x"
        
    canvas.create_text(
        276.0,
        381.0,
        anchor="nw",
        text=f"Pixel Sum   : {pixel_sum}",
        fill="#000000",
        font=("Courier", 14)
    )
    
        
    canvas.create_text(
        277.0,
        407.0,
        anchor="nw",
        text=f"Width       : {width}",
        fill="#000000",
        font=("Courier", 14)
    )

    canvas.create_text(
        275.0,
        431.0,
        anchor="nw",
        text=f"Height      : {height}",
        fill="#000000",
        font=("Courier", 14)
    )

    
    canvas.create_text(
        275.0,
        455.0,
        anchor="nw",
        text=f"Bit depth   : {bit_depth}",
        fill="#000000",
        font=("Courier", 14)
    )


    canvas.create_text(
        40.0,
        11.0,
        anchor="nw",
        text="Details",
        fill="#000000",
        font=("Courier", 14)
    )

    root.bind('<Escape>', lambda e: back_to_login())
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
    file_path1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    if not file_path1:
        print("file not selected")
    else:
        img1 = Image.open(file_path1)
        img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
        scanner = Scanner()
        row = scanner.match_in_db(img1)
        load_ui(row)
            