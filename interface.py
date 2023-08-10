from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from sql_ph import DBM

root = Tk()
position_right = int((root.winfo_screenwidth() * (1 / 5)))
position_down = int((root.winfo_screenheight() * (1 / 5)))
standar_position = "+{}+{}".format(position_right, position_down)
photo = None



class MiApp:

    def __init__(self, master: Tk):
        self.master = master
        self.master.title('PH ABM')
        self.master.config(bg="white")
        self.master.iconbitmap(r'ph_icon.ico')
        self.details_top = None
        self.main_root()

    def main_root(self):
        global photo
        self.master.geometry('480x320'+standar_position)
        self.master.rowconfigure(0, minsize=20)
        self.master.rowconfigure(1, weight=5)
        self.master.rowconfigure(2, weight=5)
        self.master.rowconfigure(3, weight=5)
        self.master.columnconfigure(0, minsize=10)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=10)

        # Label simple
        image = Image.open("ph_logo.jpg")
        image = image.resize((90, 90))
        photo = ImageTk.PhotoImage(image)
        frame_logo = Frame(self.master)
        frame_logo.grid(row=1, column=1, rowspan=2)
        Label(frame_logo, image=photo).pack(expand=YES, anchor="nw")

        Button(self.master, text="Ver Recetas",
               command=lambda: self.__go2__("Recipes")).grid(row=1, column=2)
        Button(self.master, text="Ver Materia Prima",
               command=lambda: self.__go2__("Ingredients")).grid(row=2, column=2)
        Button(self.master, text="Ver Material de Empaque",
               command=lambda: self.__go2__("Packagings")).grid(row=3, column=2)

    def recipe_root(self):
        global photo
        self.master.geometry('900x480')
        self.master.rowconfigure(0, minsize=20)
        self.master.rowconfigure(1, weight=2)
        self.master.rowconfigure(1, weight=2)
        self.master.rowconfigure(2, weight=2)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=8)
        self.master.rowconfigure(5, weight=3)
        self.master.columnconfigure(0, minsize=10)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=5)
        self.master.columnconfigure(3, weight=4)
        self.master.columnconfigure(4, weight=2)

        # Label Simple
        image = Image.open("ph_logo.jpg")
        image = image.resize((90, 90))
        photo = ImageTk.PhotoImage(image)
        logo_frame = Frame(self.master, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        # Table Recipe
        table_frame = Frame(self.master, bg="white")
        table_frame.grid(row=3, column=2, sticky="nsew", rowspan=2)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table = ttk.Treeview(table_frame)
        table['columns'] = ('id',
                            'name',
                            'price',
                            'units',
                            'details',
                            'delete')

        def __on_table_click__(event):
            col = table.identify_column(event.x)
            recipe_name = table.item(table.selection()[0], 'values')[1]
            match col:
                case '#5':
                    """Detalles de la receta"""
                    print(recipe_name)
                    self.details_recipe_windows()
                case '#6':
                    """Eliminar receta"""
                    print("Eliminar")
                case _:
                    pass

        table.column('#0', width=0, stretch=NO)
        table.column('id', width=40, anchor=CENTER)
        table.column('name', anchor=CENTER)
        table.column('price', width=100, anchor=CENTER)
        table.column('units', width=100, anchor=CENTER)
        table.column('details', width=12, anchor=CENTER)
        table.column('delete', width=12, anchor=CENTER)
        table.heading('id', text="ID", anchor=CENTER)
        table.heading('name', text="Receta", anchor=CENTER)
        table.heading('price', text="Precio C/U", anchor=CENTER)
        table.heading('units', text="Cantidad", anchor=CENTER)
        all_recipes = DBM.query_get_all_recipes()
        if len(all_recipes) != 0:
            for recipe in all_recipes:
                recipe_row = [recipe.id, recipe.name,
                              recipe.price_for_unit(), recipe.units,
                              "📝",
                              "  🗑️"]
                table.insert(parent='', index='end', values=recipe_row)
        table.grid(row=0, column=0, sticky="nsew")
        table.bind('<ButtonRelease-1>', __on_table_click__)

    def ingredients_root(self):
        global photo
        self.master.geometry('900x500')
        self.master.rowconfigure(0, minsize=20)
        self.master.rowconfigure(1, weight=2)
        self.master.rowconfigure(1, weight=2)
        self.master.rowconfigure(2, weight=2)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=8)
        self.master.rowconfigure(5, weight=3)
        self.master.columnconfigure(0, minsize=10)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=5)
        self.master.columnconfigure(3, weight=2)

        # Label Simple
        image = Image.open("ph_logo.jpg")
        image = image.resize((90, 90))
        photo = ImageTk.PhotoImage(image)
        logo_frame = Frame(self.master, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        # Table Recipe
        table_frame = Frame(self.master, bg="red")
        table_frame.grid(row=3, column=2, sticky="nsew", rowspan=2)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table = ttk.Treeview(table_frame)
        table['columns'] = ('id', 'name', 'price', 'type', 'info', 'modify', 'delete')
        table.column('#0', width=0, stretch=NO)
        table.column('#0', width=0, stretch=NO)
        table.column('id', width=40, anchor=CENTER)
        table.column('name', anchor=CENTER)
        table.column('price', width=100, anchor=CENTER)
        table.column('type', width=40, anchor=CENTER)
        table.column('info', width=12, anchor=CENTER)
        table.column('modify', width=12, anchor=CENTER)
        table.column('delete', width=12, anchor=CENTER)
        table.heading('id', text="ID", anchor=CENTER)
        table.heading('name', text="Ingrediente", anchor=CENTER)
        table.heading('price', text="Precio", anchor=CENTER)
        table.heading('type', text="Medida", anchor=CENTER)
        all_ingredients = DBM.query_get_all_ingredients()
        if len(all_ingredients) != 0:
            for ingredient in all_ingredients:
                table.insert(parent='', index='end', values=ingredient.as_tuple())
        table.grid(row=0, column=0, sticky="nsew")

    def packagings_root(self):
        pass

    def details_recipe_windows(self):
        self.details_top: Toplevel = Toplevel(self.master)
        self.details_top.title("Detalles de la receta")
        self.details_top.iconbitmap("ph_icon.ico")
        self.__set_toplevel__()




    def __go2__(self, where: str):
        go2window = {
            "Recipes": lambda: self.recipe_root(),
            "Ingredients": lambda: self.ingredients_root(),
            "Packagings": lambda: self.packagings_root(),
            "Main": lambda: self.main_root()
        }
        for widget in self.master.winfo_children():
            widget.destroy()
        go2window[where]()

    def __on_closing_toplevel__(self):
        self.details_top.destroy()
        self.details_top = None

    def __set_toplevel__(self, geometry_size: str = "320x320"):
        window_width = self.details_top.winfo_reqwidth()
        window_height = self.details_top.winfo_reqheight()
        position_t_right = int(position_right + (window_height / 1))
        position_t_down = int(position_down + (window_width / 2))
        toplevel_posi
        self.details_top.geometry(f'{geometry_size}'+'+{}+{}'.format(position_t_right, position_t_down))
        self.details_top.resizable(False, False)
        self.details_top.grab_set()


def main():
    MiApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
