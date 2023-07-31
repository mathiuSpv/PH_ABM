from tkinter import *
from PIL import Image, ImageTk
import os

folder_path = os.path.dirname(os.path.abspath(__file__))
window = Tk()

window.title('PH AMB')
window.config(bg="white")
window.geometry('720x480')
window.iconbitmap(r'ph_icon.ico')


frame00 = Frame(window, bg="white")
frame00.grid(row=0, column=0, sticky="nsew")
image = Image.open('ph_logo.jpg')
photo = ImageTk.PhotoImage(image)
label = Label(frame00, image=photo)
label.pack()

window.columnconfigure(0, minsize=120)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)
window.rowconfigure(0, minsize=20)
window.rowconfigure(1, weight=2)
window.rowconfigure(2, weight=2)


#Añadir botones
def add_buttons():
    colors_mat= {0: 'red',
                 1: 'green',
                 2: 'blue',
                 10: 'yellow',
                 11: 'purple',
                 12: 'black'
    }
    for i in range(3):
        frame = Frame(window, bg=f'{colors_mat[i]}')
        frame.grid(row=i, column=1, sticky="nsew")
        j= i + 10
        frame_next = Frame(window, bg=f'{colors_mat[j]}')
        frame_next.grid(row=i, column=2, sticky="nsew")

        button = Button(frame, text=f"Boton{i}")
        button.pack()
        button_next = Button(frame_next, text=f"Button {i+3}")
        button_next.pack()


add_buttons()
image = Image.open('ph_logo.jpg')
photo = ImageTk.PhotoImage(image)
label = Label(window, image=photo)
label.place(x=0, y=0)
window.mainloop()
