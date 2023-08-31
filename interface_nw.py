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


def clear_root():
    for widget in root.winfo_children():
        widget.destroy()
    for i in range(root.grid_size()[0]):
        root.columnconfigure(i, weight=0)
    for i in range(root.grid_size()[1]):
        root.rowconfigure(i, weight=0)


def window_format(windows_object,
                  geometry_size: str = "180x110",
                  padx: int = 0, pady: int = 0):
    window_width = windows_object.winfo_reqwidth()
    window_height = windows_object.winfo_reqheight()
    position_t_right = int(position_right + (window_height / 1))
    position_t_down = int(position_down + (window_width / 2))
    windows_object.geometry(f'{geometry_size}' + '+{}+{}'.format(padx + position_t_right,
                                                                 pady + position_t_down))
    windows_object.resizable(False, False)
    windows_object.grab_set()


def go2main():
    clear_root()
    main_section.show()


def go2recipes():
    clear_root()
    recipes_section.show()


def go2ingredients():
    clear_root()
    ingredients_section.show()


def go2packagings():
    clear_root()
    packagings_section.show()


class mainRoot:
    def __init__(self):
        self.show()

    def show(self):
        """Vision completa"""
        # CONFIGURACION
        root.title('PH ABM - Inicio')
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

        # INSERTAR
        global photo
        frame_logo = Frame(root)
        frame_logo.grid(row=1, column=1, sticky="nw")
        Label(frame_logo, image=photo).pack(anchor="nw")

        Button(root, text="Ver \nRecetas",
               command=go2recipes, width=18
               ).grid(row=1, column=2, sticky="n", pady=10)
        Button(root, text="Ver \nMateria Prima",
               command=go2ingredients, width=18
               ).grid(row=1, column=2, sticky="", pady=20)
        Button(root, text="Ver \nMaterial de Empaque",
               command=go2packagings, width=18
               ).grid(row=1, column=2, sticky="s", pady=10)


def root_config():
    root.geometry('900x480')
    root.iconbitmap(r'ph_icon.ico')
    root.rowconfigure(0, minsize=20)
    root.rowconfigure(1, weight=2)
    root.rowconfigure(2, weight=2)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=8)
    root.rowconfigure(5, weight=3)
    root.columnconfigure(0, minsize=10)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=5)
    root.columnconfigure(3, weight=4)
    root.columnconfigure(4, minsize=10)


class Section:
    def __init__(self):
        self.table = None
        self.details = None


class recipesRoot(Section):
    def __init__(self):
        super().__init__()

    def show(self):
        # CONFIGURACION
        root_config()
        root.title('PH ABM - Recetas')

        # FUNCIONES
        def table_recipe_config():
            """Definicion de Columnas y Headings de el 'self.table'"""
            self.table.column('#0', width=0, stretch=NO)
            self.table.column('id', width=40, anchor=CENTER)
            self.table.column('name', anchor=CENTER)
            self.table.column('price', width=120, anchor=CENTER)
            self.table.column('units', width=100, anchor=CENTER)
            self.table.column('details', width=16, anchor=CENTER)
            self.table.column('delete', width=16, anchor=CENTER)
            self.table.heading('id', text="ID", anchor=CENTER)
            self.table.heading('name', text="Nombre de la Receta", anchor=CENTER)
            self.table.heading('price', text="Precio", anchor=CENTER)
            self.table.heading('units', text="Cantidad", anchor=CENTER)

        def table_recipe_insert(param = DBM.query_get_all_recipes()):
            for row in self.table.get_children():
                self.table.delete(row)

            for recipe in param:
                recipe_row = (recipe.id, recipe.name,
                              recipe.price_for_unit(), recipe.units,
                              "📝", " 🗑️")
                self.table.insert("", "end", values=recipe_row)

        def on_key_release(event):
            def filter_by_name():
                content = entry_name.get()
                try:
                    entry_name.delete(0, END)
                    entry_name.insert(0, f"{content[0].upper()}{content[1::].lower()}")
                except IndexError:
                    entry_name.insert(0, content)
                return entry_name.get()

            def filter_by_id():
                return entry_id.get()

            _id = filter_by_id()
            _name = filter_by_name()
            if _id or _name:
                if _id:
                    pass
                else:
                    pass
            else:
                r = DBM.query_get_all_recipes()

        # ENTRY Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table['columns'] = ('id',
                                 'name',
                                 'price',
                                 'units',
                                 'details',
                                 'delete')

        table_recipe_config()
        entry_id = Entry(root)
        entry_name = Entry(root)
        entry_id.config(validate='key', validatecommand=(root.register(
            lambda P: True if P == "" or (
                    P.isdigit()
                    and len(P) <= 3) else False), "%P"),
                        width=5)
        entry_name.config(validate="key", validatecommand=(root.register(
            lambda P: True if P == "" or len(P) <= 32 else False), "%P"),
                          width=25)

        add_recipe = Button(root, bg="white", text="Añadir \nReceta", width=20, height=2)

        # GRIDS Y BINDS
        Label(root, text="ID", bg="white").grid(row=2, column=2, sticky="sw", padx=20, pady=26)
        Label(root, text="Nombre", bg="white").grid(row=2, column=2, sticky="sw", padx=120, pady=26)
        self.table.grid(row=3, column=2, sticky="nsew", rowspan=2)
        entry_id.grid(row=2, column=2, sticky="sw", padx=10, pady=5)
        entry_name.grid(row=2, column=2, sticky="sw", padx=80, pady=5)
        add_recipe.grid(row=3, column=3, sticky="s")
        Button(root, bg="white", text="Volver a Inicio", width=16, height=1,
               command=go2main).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)
        Button(root, bg="white", text="Ir a Materia Prima", width=16, height=1,
               command=go2ingredients).grid(row=1, column=2, columnspan=2, sticky="w", padx=150)
        Button(root, bg="white", text="Ir a Empaquetados", width=16, height=1,
               command=go2packagings).grid(row=1, column=2, columnspan=2, sticky="w", padx=150 * 2)

        table_recipe_insert()
        entry_id.bind("<KeyRelease>", on_key_release)
        entry_name.bind("<KeyRelease>", on_key_release)


class ingredientsRoot(Section):
    """PANTALLA DE INGREDIENTES CON SUS FUNCIONALIDADES"""

    def __init__(self):
        super().__init__()

    def show(self):
        # CONFIGURACION
        root_config()
        root.title('PH ABM - Materia Prima')

        # ENTRY Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table['columns'] = ('id',
                                 'name',
                                 'price',
                                 'type',
                                 'details',
                                 'delete')

        def table_ingredient_config():
            self.table.column('#0', width=0, stretch=NO)
            self.table.column('id', width=40, anchor=CENTER)
            self.table.column('name', anchor=CENTER)
            self.table.column('price', width=120, anchor=CENTER)
            self.table.column('type', width=100, anchor=CENTER)
            self.table.column('details', width=16, anchor=CENTER)
            self.table.column('delete', width=16, anchor=CENTER)
            self.table.heading('id', text="ID", anchor=CENTER)
            self.table.heading('name', text="Materia Prima", anchor=CENTER)
            self.table.heading('price', text="Costo", anchor=CENTER)
            self.table.heading('type', text="Medida", anchor=CENTER)

        table_ingredient_config()
        entry_id.config(validate='key', validatecommand=(root.register(
            lambda P: True if P == "" or (
                    P.isdigit()
                    and len(P) <= 3) else False), "%P"),
                        width=5)
        entry_name.config(validate="key", validatecommand=(root.register(
            lambda P: True if P == "" or len(P) <= 32 else False), "%P"),
                          width=25)

        add_ingredient = Button(root, bg="white", text="Añadir \nIngrediente", width=20, height=2)
        back_mainmenu = Button(root, bg="white", text="Volver a Menu", width=16, height=1,
                               command=go2main)
        go_recipe = Button(root, bg="white", text="Ir a Recetas", width=16, height=1,
                           command=go2recipes)
        go_packaging = Button(root, bg="white", text="Ir a Empaquetado", width=16, height=1,
                              command=go2packagings)

        # GRIDS Y BINDS
        Label(root, text="ID", bg="white").grid(row=2, column=2, sticky="sw", padx=20, pady=26)
        Label(root, text="Nombre", bg="white").grid(row=2, column=2, sticky="sw", padx=120, pady=26)
        self.table.grid(row=3, column=2, sticky="nsew", rowspan=2)
        entry_id.grid(row=2, column=2, sticky="sw", padx=10, pady=5)
        entry_name.grid(row=2, column=2, sticky="sw", padx=80, pady=5)
        add_ingredient.grid(row=3, column=3, sticky="s")
        Button(root, bg="white", text="Volver a Inicio", width=16, height=1,
               command=go2main).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)
        go_recipe.grid(row=1, column=2, columnspan=2, sticky="w", padx=150)
        Button(root, bg="white", text="Ir a Empaquetados", width=16, height=1,
               command=go2packagings).grid(row=1, column=2, columnspan=2, sticky="w", padx=150 * 2)


class packagingsRoot(Section):
    def __init__(self):
        super().__init__()

    def show(self):
        # CONFIGURACION
        root_config()
        root.title('PH ABM - Material de Empaque')

        # ENTRYS Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table['columns'] = ('id',
                                 'name',
                                 'cost',
                                 'profit',
                                 'details',
                                 'delete')

        def table_packaging_config():
            self.table.column('#0', width=0, stretch=NO)
            self.table.column('id', width=40, anchor=CENTER)
            self.table.column('name', anchor=CENTER)
            self.table.column('cost', width=120, anchor=CENTER)
            self.table.column('profit', width=100, anchor=CENTER)
            self.table.column('details', width=16, anchor=CENTER)
            self.table.column('delete', width=16, anchor=CENTER)
            self.table.heading('id', text="ID", anchor=CENTER)
            self.table.heading('name', text="Material de Empaque", anchor=CENTER)
            self.table.heading('cost', text="Costo", anchor=CENTER)
            self.table.heading('profit', text="Beneficio", anchor=CENTER)

        table_packaging_config()
        entry_id.config(validate='key', validatecommand=(root.register(
            lambda P: True if P == "" or (
                    P.isdigit()
                    and len(P) <= 3) else False), "%P"),
                        width=5)
        entry_name.config(validate="key", validatecommand=(root.register(
            lambda P: True if P == "" or len(P) <= 32 else False), "%P"),
                          width=25)

        add_packaging = Button(root, bg="white", text="Añadir \nEmpaque", width=20, height=2)
        back_mainmenu = Button(root, bg="white", text="Volver a Menu", width=16, height=1,
                               command=go2main)
        go_recipe = Button(root, bg="white", text="Ir a Receta", width=16, height=1,
                           command=go2recipes)
        go_ingredient = Button(root, bg="white", text="Ir a Materia Prima", width=16, height=1,
                               command=go2ingredients)

        # GRID Y BINDS
        Label(root, text="ID", bg="white").grid(row=2, column=2, sticky="sw", padx=20, pady=26)
        Label(root, text="Nombre", bg="white").grid(row=2, column=2, sticky="sw", padx=120, pady=26)
        self.table.grid(row=3, column=2, sticky="nsew", rowspan=2)
        entry_id.grid(row=2, column=2, sticky="sw", padx=10, pady=5)
        entry_name.grid(row=2, column=2, sticky="sw", padx=80, pady=5)
        add_packaging.grid(row=3, column=3, sticky="s")
        Button(root, bg="white", text="Volver a Inicio", width=16, height=1,
               command=go2main).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)
        go_recipe.grid(row=1, column=2, columnspan=2, sticky="w", padx=150)
        go_ingredient.grid(row=1, column=2, columnspan=2, sticky="w", padx=150 * 2)


# main_section = mainRoot()
recipes_section = recipesRoot()
ingredients_section = ingredientsRoot()
packagings_section = packagingsRoot()
if __name__ == "__main__":
    recipes_section.show()
    pass

root.mainloop()
