from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from sql_ph import DBM


# import sys, os
# sys.path.append(os.getcwd())

class MiApp:

    def __init__(self, master: Tk):

        self.master = master
        self.master.title('PH AMB')
        self.master.config(bg="white")
        self.master.iconbitmap(r'ph_icon.ico')
        self.main_root()

    def main_root(self):
        global photo
        self.master.geometry('480x320')
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
        table['columns'] = ('id', 'name', 'price', 'ingredients', 'packagings', 'modify', 'delete')
        table.column('#0', width=0, stretch=NO)
        table.column('#0', width=0, stretch=NO)
        table.column('id', width=40, anchor=CENTER)
        table.column('name', anchor=CENTER)
        table.column('price', width=100, anchor=CENTER)
        table.column('ingredients', width=12, anchor=CENTER)
        table.column('modify', width=12, anchor=CENTER)
        table.column('delete', width=12, anchor=CENTER)
        table.heading('id', text="ID", anchor=CENTER)
        table.heading('name', text="Receta", anchor=CENTER)
        table.heading('price', text="Precio", anchor=CENTER)
        all_recipes = DBM.query_get_all_recipes()
        if len(all_recipes) != 0:
            for recipe in all_recipes:
                recipe = [recipe.id, recipe.name, recipe.price_for_unit()]
                table.insert(parent='', index='end', values=recipe)
        table.grid(row=0, column=0, sticky="nsew")


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

    def __go2__(self, where: str):
        go2window = {
            "Recipes": lambda: self.recipe_root(),
            "Ingredients": lambda: self.ingredients_root(),
            "Main": lambda: self.main_root()
        }
        for widget in self.master.winfo_children():
            widget.destroy()
        go2window[where]()



def main():
    root = Tk()
    app = MiApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
