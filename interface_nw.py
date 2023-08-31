from tkinter import *
from tkinter import Tk, ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from sql_ph import DBM, Recipes, Ingredients, Packagings

root = ThemedTk(theme="breeze")
position_right = int((root.winfo_screenwidth() * (1 / 5)))
position_down = int((root.winfo_screenheight() * (1 / 5)))
standar_position = "+{}+{}".format(position_right, position_down)
image = Image.open("ph_logo.jpg")
image = image.resize((90, 90))
photo = ImageTk.PhotoImage(image)


class standardFuntions:
    def clear_root(self):
        for widget in root.winfo_children():
            widget.destroy()
        for i in range(root.grid_size()[0]):
            root.columnconfigure(i, weight=0)
        for i in range(root.grid_size()[1]):
            root.rowconfigure(i, weight=0)
    
    def window_format(self,
                      windows_object: Tk,
                      geometry_size: str = "380x380",
                      padx: int = 0, pady: int = 0):
        window_width = windows_object.winfo_reqwidth()
        window_height = windows_object.winfo_reqheight()
        position_t_right = int(position_right + (window_height / 1))
        position_t_down = int(position_down + (window_width / 2))
        windows_object.geometry(f'{geometry_size}' + '+{}+{}'.format(padx + position_t_right,
                                                                    pady + position_t_down))
        windows_object.resizable(False, False)
        windows_object.grab_set()
    
    def go2main(self):
        self.clear_root()
        main_section.show()
    
    def go2recipes(self):
        self.clear_root()
        recipes_section.show()
    
    def go2ingredients(self):
        self.clear_root()
        ingredients_section.show()
    
    def go2packagings(self):
        self.clear_root()
        packagings_section.show()
        
    def custom_confirm(self, text : str):
        def __on_key_amount__(event):
            content = entry_value.get()
            if event.keysym.isnumeric():
                match len(content):
                    case 2:
                        entry_value.delete(0, END)
                        entry_value.insert(0, f"{content}.0")
                    case 4:
                        entry_value.delete(0, END)
                        entry_value.insert(0, f"{content[:3:]}{event.keysym}")
            elif event.keysym == "period" and len(content) == 1:
                entry_value.delete(0, END)
                entry_value.insert(0, f"0.")
            elif event.keysym == "BackSpace":
                if len(content) > 0:
                    content_r = len(content) - 1
                    entry_value.delete(0, END)
                    entry_value.insert(0, f"{content[:content_r:]}")
            elif event.keysym == "Return":
                __func_button_confirm__()
            elif event.keysym == "Escape":
                response.destroy()

        def __func_button_confirm__():
            try:
                amount = float(entry_value.get())
                response.destroy()
            except ValueError:
                pass
            except Exception as e:
                print(type(e).__name__)
                pass

        response = Toplevel(self.details_top)
        response.title("")
        response.iconbitmap('ph_icon.ico')
        self.window_format(response, geometry_size="180x110", padx=100, pady=40)
        response.rowconfigure(0, weight=5)
        response.rowconfigure(1, weight=2)
        response.columnconfigure(0, weight=2)
        Label(response,
                text=text
                ).grid(row=0, column=0, sticky="n", pady=2)
        entry_value = Entry(response,
                            validate="key",
                            validatecommand=(self.details_top.register(
                                lambda P: True if P == "" or (
                                        not P.isalpha()
                                        and len(P) <= 4) else False), "%P"),
                            width=5)
        entry_value.grid(row=0, column=0, sticky="s")
        confirm_button = Button(response,
                                text="Confirmar Cambio",
                                command=__func_button_confirm__)
        confirm_button.grid(row=1, column=0, sticky="")
        entry_value.bind("<KeyRelease>", __on_key_amount__)
    
    
class mainRoot(standardFuntions):
    def __init__(self):
        self.main_view()
        
    def main_view(self):
        """Vision completa"""
        #CONFIGURACION
        root.title('PH ABM')
        root.config(bg='white')
        root.iconbitmap(r'ph_icon.ico')
        root.geometry('480x320' + standar_position)
        root.rowconfigure(0, minsize=20)
        root.rowconfigure(1, weight=2)
        root.rowconfigure(2, weight=2)
        root.columnconfigure(0, minsize=20)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=7)
        root.columnconfigure(3, minsize=20)
        
        #INSERTAR
        global photo
        frame_logo = Frame(root)
        frame_logo.grid(row=1, column=1, sticky="nw")
        Label(frame_logo, image=photo).pack(anchor="nw")

        Button(root, text="Ver \nRecetas",
               command=self.go2recipes, width=18
               ).grid(row=1, column=2, sticky="n", pady=10)
        Button(root, text="Ver \nMateria Prima",
               command=self.go2ingredients, width=18
               ).grid(row=1, column=2, sticky="", pady=20)
        Button(root, text="Ver \nMaterial de Empaque",
               command=self.go2packagings, width=18
               ).grid(row=1, column=2, sticky="s", pady=10)

class recipesRoot(standardFuntions):
    def __init__(self):
        self.details= None
        self.recipe_view()
        
    def recipe_view(self):
        pass

class ingredientsRoot(standardFuntions):
    def __init__(self):
        self.details= None

class packagingsRoot(standardFuntions):
    def __init__(self):
        self.details= None
        
    

main_section = mainRoot()
recipes_section = recipesRoot()
ingredients_section  = ingredientsRoot()
packagings_section = packagingsRoot()

root.mainloop()