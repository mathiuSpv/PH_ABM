from tkinter import *
from PIL import Image, ImageTk

root = Tk()
photos = None
images = {'ph_image': Image.open("ph_logo.jpg")}

def main_menu():
    global root, photo
    root.title('PH AMB')
    root.config(bg="white")
    root.geometry('480x320')
    root.iconbitmap(r'ph_icon.ico')
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=2)
    root.rowconfigure(3, weight=2)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=5)

    #Label simple
    image = Image.open("ph_logo.jpg")
    image = image.resize((120, 100))
    photo = ImageTk.PhotoImage(image)
    frame_logo = Frame(root, bg="white")
    frame_logo.grid(row=0, column=0, sticky="nsew")
    Label(frame_logo, image=photo).pack(expand=YES, anchor="nw")

    Label(root, text="Texto 1", bg="blue").grid(row=0, column=1, sticky="nsew")
    Label(root, text="Texto 3", bg="red").grid(row=1, column=0, columnspan=2, sticky="nsew")
    Label(root, text="Texto 3", bg="red").grid(row=2, column=0, sticky="nsew")
    Label(root, text="Texto 4", bg="orange").grid(row=2, column=1, sticky="nsew")
    Label(root, text="Texto 4", bg="green").grid(row=3, column=0, sticky="nsew")
    Label(root, text="Texto 4", bg="purple").grid(row=3, column=1, sticky="nsew")


main_menu()
root.mainloop()
