from tkinter import *
from tkinter import Tk, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from sql_ph import DBM, Recipes, Ingredients, Packagings, IngredientsRecipes

restart_color = "#2C9CF5"
confirm_color = "#07D63D"
decline_color = "#E32714"

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
                  padx: int = 0, pady: int = 0,
                  resizable=False, grab_set=False):
    window_width = windows_object.winfo_reqwidth()
    window_height = windows_object.winfo_reqheight()
    position_t_right = int(position_right + (window_height / 1))
    position_t_down = int(position_down + (window_width / 2))
    windows_object.geometry(f"{geometry_size}" + "+{}+{}".format(padx + position_t_right,
                                                                 pady + position_t_down))
    if resizable:
        windows_object.resizable(False, False)
    if grab_set:
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


def custom_confirm(windows, text: str = ""):
    response = Toplevel(windows)
    response.title("")
    response.iconbitmap("ph_icon.ico")
    window_format(response, geometry_size="180x105", padx=100, pady=40, resizable=True, grab_set=True)
    response.rowconfigure(0, weight=2)
    response.rowconfigure(1, weight=1)
    response.columnconfigure(0, weight=2)
    Label(response,
          text=text).grid(
        row=0, column=0, sticky="nwse", pady=2)
    yes = Button(response, bg="white", text="Si", padx=12, pady=2)
    no = Button(response, bg="white", text="No", padx=12, pady=2)
    yes.grid(row=1, column=0, sticky="w", padx=12, pady=5)
    no.grid(row=1, column=0, sticky="e", padx=12, pady=5)
    return response, yes, no


def custom_amount(windows, text: str = "", max_int: int = 2):
    def on_amount(event):
        content = entry_value.get()
        if event.keysym.isnumeric():
            array_long = len(content)
            if array_long == max_int:
                entry_value.delete(0, END)
                entry_value.insert(0, f"{content}.0")
            elif array_long == max_int + 2:
                entry_value.delete(0, END)
                entry_value.insert(0, f"{content[:max_int:]}.{event.keysym}")
            elif array_long > max_int and content[max_int] != ".":
                entry_value.delete(0, END)
                entry_value.insert(0, f"{content[:max_int:]}.{content[max_int::]}")
        elif event.keysym == "period" and len(content) == 1:
            entry_value.delete(0, END)
            entry_value.insert(0, f"0.")
        elif event.keysym == "BackSpace" and len(content) > 0 and content[len(content) - 1] == ".":
            entry_value.delete(0, END)
            entry_value.insert(0, f"{content[:len(content) - 1:]}")
        elif event.keysym == "Return":
            confirm_verification()
        elif event.keysym == "Escape":
            entry_value.delete(0, END)
            response.destroy()

    def confirm_verification():
        try:
            value = float(entry_value.get())
            entry_value.delete(0, END)
            entry_value.insert(0, f"{value}")
            response.destroy()
        except ValueError:
            Label(response, text="Valor invalido", foreground='red'
                  ).grid(row=0, column=0, sticky="s", pady=4)

    response = Toplevel(windows)
    response.title("")
    response.iconbitmap('ph_icon.ico')
    window_format(response, geometry_size="200x115", padx=100, pady=40, resizable=True, grab_set=True)
    response.rowconfigure(0, weight=2)
    response.rowconfigure(1, weight=2)
    response.columnconfigure(0, weight=2)
    Label(response, text=text).grid(row=0, column=0, sticky="n", pady=2)

    Button(response,
           text="Confirmar Cambio",
           command=confirm_verification).grid(row=1, column=0, sticky="s", pady=2)
    entry_value = Entry(response,
                        validate="key",
                        validatecommand=(windows.register(
                            lambda P: True if P == "" or (
                                    not P.isalpha()
                                    and len(P) <= max_int + 2) else False), "%P"),
                        width=5)

    entry_value.focus_set()
    entry_value.grid(row=1, column=0, sticky="n")
    entry_value.bind("<KeyRelease>", on_amount)
    return response, entry_value


class mainRoot:
    def __init__(self):
        pass

    def show(self):
        """Vision completa"""
        # CONFIGURACION
        root.title("PH ABM - Inicio")
        root.config(bg="white")
        root.iconbitmap(r"ph_icon.ico")
        root.geometry("480x320" + standar_position)
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


def on_key_profit(event, entry):
    content = entry.get()
    array_long = len(content)
    if event.keysym.isnumeric():
        match array_long:
            case 3:
                entry.delete(0, END)
                entry.insert(0, f"{content[0]}.{event.keysym}")
            case 2:
                entry.delete(0, END)
                entry.insert(0, f"{content[0]}.{event.keysym}")
            case 1:
                entry.delete(0, END)
                entry.insert(0, f"{content[0]}.")
    elif event.keysym == "BackSpace":
        match array_long:
            case 2:
                entry.delete(0, END)
                entry.insert(0, f"{content[0]}")
            case 1:
                entry.delete(0, END)
    elif event.keysym == "period":
        match array_long:
            case 3:
                entry.delete(0, END)
                entry.insert(0, f"{content[0]}.0")
    else:
        index = content.rfind(event.char)
        if index >= 0:
            entry.delete(0, END)
            entry.insert(0, f"{content[:index:]}")


def on_key_name(event, entry: Entry):
    content = entry.get()
    try:
        entry.delete(0, END)
        entry.insert(0, f"{content[0].upper()}{content[1::].lower()}")
    except IndexError:
        entry.insert(0, content)


class Section:
    def __init__(self):
        self.root = root
        self.table = None
        self.details = None

    def root_config(self):
        self.root.geometry("900x480")
        self.root.iconbitmap(r"ph_icon.ico")
        self.root.rowconfigure(0, minsize=20)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=2)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=8)
        self.root.rowconfigure(5, weight=3)
        self.root.columnconfigure(0, minsize=10)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=6)
        self.root.columnconfigure(3, weight=3)
        self.root.columnconfigure(4, minsize=10)

    def on_table_click(self, event):
        col = self.table.identify_column(event.x)
        _id = self.table.item(self.table.selection()[0], "values")[0]
        _name = self.table.item(self.table.selection()[0], "values")[1]
        return col, _id, _name


class recipesRoot(Section):
    def __init__(self):
        super().__init__()

    def show(self):
        # CONFIGURACION
        self.root_config()
        root.title("PH ABM - Recetas")

        # FUNCIONES
        def table_recipe_config():
            """Definicion de Columnas y Headings de el self.table"""
            self.table.column("#0", width=0, stretch=NO)
            self.table.column("id", width=40, anchor=CENTER)
            self.table.column("name", anchor=CENTER)
            self.table.column("price", width=120, anchor=CENTER)
            self.table.column("units", width=100, anchor=CENTER)
            self.table.column("details", width=16, anchor=CENTER)
            self.table.column("delete", width=16, anchor=CENTER)
            self.table.heading("id", text="ID", anchor=CENTER)
            self.table.heading("name", text="Nombre de la Receta", anchor=CENTER)
            self.table.heading("price", text="Precio", anchor=CENTER)
            self.table.heading("units", text="Cantidad", anchor=CENTER)

        def table_recipe_insert(param):
            for row in self.table.get_children():
                self.table.delete(row)

            for recipe in param:
                recipe_row = (recipe.id, recipe.name,
                              round(recipe.price_for_unit(), 2), recipe.units,
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
            if _id and _name:
                qr = DBM.session.query(Recipes).filter(Recipes.id.like(f"%{_id}%")
                                                       ).filter(Recipes.name.like(f"%{_name}%")).all()
            elif _id:
                qr = DBM.session.query(Recipes).filter(Recipes.id.like(f"%{_id}%")).all()
            elif _name:
                qr = DBM.session.query(Recipes).filter(Recipes.name.like(f"%{_name}%")).all()
            else:
                qr = DBM.query_get_all_recipes()
            return table_recipe_insert(qr)

        def on_table(event):
            try:
                col, recipe_id, recipe_name = self.on_table_click(event)
                if col == "#5":
                    qr = DBM.query_get_recipe(recipe_name)
                    self.details_recipe(qr)
                elif col == "#6":
                    response, yes, no = custom_confirm(root,
                                                       text=f"¿ Eliminar {recipe_id} - {recipe_name} ?")
                    yes.config(command=lambda: (DBM.del_recipe(recipe_name), response.destroy()))
                    no.config(command=lambda: response.destroy())

                    def response_destroy(event):
                        update = DBM.query_get_all_recipes()
                        table_recipe_insert(update)

                    response.bind("<Destroy>", response_destroy)
            except IndexError:
                pass

        # ENTRY Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table["columns"] = ("id",
                                 "name",
                                 "price",
                                 "units",
                                 "details",
                                 "delete")

        table_recipe_config()
        entry_id = Entry(root)
        entry_name = Entry(root)
        entry_id.config(validate="key", validatecommand=(root.register(
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
        Button(root, bg="white", text="♻", background=restart_color, fg="white", width=8, height=1,
               command=lambda: (
                   entry_id.delete(0, END), entry_name.delete(0, END), table_recipe_insert(DBM.query_get_all_recipes()))
               ).grid(row=2, column=2, sticky="se", padx=240, pady=3)
        Button(root, bg="white", text="Volver a Inicio", width=16, height=1,
               command=go2main).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)
        Button(root, bg="white", text="Ir a Materia Prima", width=16, height=1,
               command=go2ingredients).grid(row=1, column=2, columnspan=2, sticky="w", padx=150)
        Button(root, bg="white", text="Ir a Empaquetados", width=16, height=1,
               command=go2packagings).grid(row=1, column=2, columnspan=2, sticky="w", padx=150 * 2)

        table_recipe_insert(DBM.query_get_all_recipes())
        self.table.bind("<ButtonRelease-1>", on_table)
        entry_id.bind("<KeyRelease>", on_key_release)
        entry_name.bind("<KeyRelease>", on_key_release)

    def details_recipe(self, recipe: Recipes):
        self.details = Toplevel(root)
        self.details.title("Detalles de la receta")
        self.details.iconbitmap("ph_icon.ico")
        self.details.config(bg="white")
        window_format(self.details, geometry_size="400x400", resizable=True, grab_set=True)
        self.details.rowconfigure(0, minsize=4)
        self.details.rowconfigure(1, minsize=24)
        self.details.rowconfigure(2, minsize=20)
        self.details.rowconfigure(3, minsize=200)
        self.details.rowconfigure(4, minsize=80)
        self.details.rowconfigure(5, minsize=2)
        self.details.columnconfigure(0, minsize=4)
        self.details.columnconfigure(1, minsize=80)
        self.details.columnconfigure(2, weight=180)
        self.details.columnconfigure(3, weight=120)
        self.details.columnconfigure(4, minsize=2)

        # FUNCIONES
        def profit_price():
            try:
                profit = float(entry_profit.get())
            except ValueError:
                profit = recipe.profit
            except NameError:
                profit = recipe.profit
            except Exception as e:
                print(type(e).__name__, e)
                profit = recipe.profit
            profit_msg = f"PRECIO DE VENTA $ {round(recipe.total_cost() * profit, 1)}"
            if recipe.units != 1:
                profit_cu = round((recipe.total_cost() * profit) / recipe.units, 1)
                profit_cu_msg = f"\n             X UNIDAD $ {profit_cu}"
            else:
                profit_cu_msg = ""
            return profit_msg + profit_cu_msg

        def db_values():
            entry_name.delete(0, END)
            entry_units.delete(0, END)
            entry_profit.delete(0, END)

            entry_name.insert(0, f"{recipe.name}")
            entry_units.insert(0, f"{recipe.units}")
            entry_profit.insert(0, f"{recipe.profit}")

        def table_recipe2ingredient_insert():
            for row in table_ingredients2recipe.get_children():
                table_ingredients2recipe.delete(row)

            ingredients2recipe = DBM.query_get_all_ingredients2recipe(recipe.name)
            for ingredient, ingredient_amount in ingredients2recipe:
                ingredient_row = (ingredient.id, ingredient.name,
                                  f"{ingredient_amount}{ingredient.unit_type}",
                                  "📝", " 🗑️")
                table_ingredients2recipe.insert(parent='', index='end', values=ingredient_row)
            label_total_cost.config(text=f"COSTO TOTAL $ {recipe.total_cost()}")
            profit_label.config(text=profit_price())

        def on_table(event):
            try:
                col = table_ingredients2recipe.identify_column(event.x)
                ingredient_id = table_ingredients2recipe.item(table_ingredients2recipe.selection()[0], "values")[0]
                ingredients_name = table_ingredients2recipe.item(table_ingredients2recipe.selection()[0], "values")[1]
                if col == "#4":
                    response, value = custom_amount(self.details,
                                                    text=f"Cambiar cantidad:\n{ingredients_name} en {recipe.name}")

                    def response_destroy(event):
                        try:
                            amount = float(value.get())
                            DBM.mdf_amount_ingredient2recipe(recipe.name, ingredients_name, amount)
                        except TclError:
                            pass
                        except ValueError:
                            pass
                        finally:
                            table_recipe2ingredient_insert()

                    response.bind("<Destroy>", response_destroy)
                elif col == "#5":
                    response, yes, no = custom_confirm(self.details,
                                                       text=f"Eliminar:\n{ingredients_name} en {recipe.name}")
                    yes.config(command=lambda: (DBM.remove_ingredient2recipe(recipe.name, ingredients_name),
                                                response.destroy()))
                    no.config(command=lambda: response.destroy())

                    def response_destroy(event):
                        table_recipe2ingredient_insert()

                    response.bind("<Destroy>", response_destroy)

            except IndexError:
                pass

        def on_profit(event, entry: Entry):
            on_key_profit(event, entry)
            profit_label.config(text=profit_price())

        def add_ingredient2recipe_button():
            ingredients_array = DBM.session.query(Ingredients).filter(
                                ~Ingredients.id.in_([Ingredients.id for b in recipe.ingredients])
                            ).all()
            """session.query(B).filter(~session.query(C).filter(C.a_id == elea.id).exists())"""
            for ingredients in DBM.query_get_all_ingredients():
                print(ingredients.name)

        # ENTRY Y BOTONES
        entry_name = Entry(self.details,
                           validate="key",
                           validatecommand=(self.details.register(
                               lambda P: True if P == "" or len(P) <= 32 else False), "%P"),
                           width=16)
        entry_units = Entry(self.details,
                            validate="key",
                            validatecommand=(self.details.register(
                                lambda P: True if P == "" or (
                                        P.isdigit() and len(P) <= 2) else False), "%P"),
                            width=3)
        entry_profit = Entry(self.details,
                             validate="key",
                             validatecommand=(self.details.register(
                                 lambda P: True if P == "" or (
                                         P[0].isnumeric() and len(P) <= 3) else False), "%P"),
                             width=4)
        label_total_cost = Label(self.details, text=f"COSTO TOTAL ${recipe.total_cost()}", bg="white")
        profit_label = Label(self.details, text=profit_price(), bg="white")
        table_ingredients2recipe = ttk.Treeview(self.details)
        table_ingredients2recipe['columns'] = ('id',
                                               'name',
                                               'quantity',
                                               'edit',
                                               'delete')
        table_ingredients2recipe.column('#0', width=0, stretch=NO)
        table_ingredients2recipe.column('id', width=36, anchor=CENTER)
        table_ingredients2recipe.column('name', width=112, anchor=CENTER)
        table_ingredients2recipe.column('quantity', width=72, anchor=CENTER)
        table_ingredients2recipe.column('edit', width=24, anchor=CENTER)
        table_ingredients2recipe.column('delete', width=24, anchor=CENTER)
        table_ingredients2recipe.heading("id", text="ID")
        table_ingredients2recipe.heading("name", text="Ingredientes")
        table_ingredients2recipe.heading("quantity", text="Cantidad")
        button_add_ingredient2recipe = Button(self.details, text="Añadir\nMateria Prima",
                                              command=add_ingredient2recipe_button)

        # GRIDS Y BINDS
        Label(self.details, text="ID", bg="white"
              ).grid(row=1, column=1, sticky="w", padx=12)
        Label(self.details, text=f"{recipe.id}", bg="white"
              ).grid(row=2, column=1, sticky="nw", padx=14)
        Label(self.details, text="NOMBRE", bg="white"
              ).grid(row=1, column=1, sticky="e", padx=38)
        Label(self.details, text="UNIDADES", bg="white"
              ).grid(row=1, column=2, sticky="w")
        Label(self.details, text="X BENEFICIO", bg="white"
              ).grid(row=4, column=1, sticky="e", padx=50)

        entry_name.grid(row=2, column=1, sticky="ne", padx=16)
        entry_units.grid(row=2, column=2, sticky="nw", padx=26)
        entry_profit.grid(row=4, column=1, sticky="e", padx=12)
        label_total_cost.grid(row=4, column=1, rowspan=2, sticky="ne")
        profit_label.grid(row=4, column=2, columnspan=2, sticky="w")
        table_ingredients2recipe.grid(row=3, column=1, sticky="w", columnspan=2, pady=4)
        button_add_ingredient2recipe.grid(row=3, column=3, sticky="n", padx=4, pady=42)

        table_ingredients2recipe.bind('<ButtonRelease-1>', on_table)
        entry_name.bind("<KeyRelease>", lambda event: on_key_name(event, entry=entry_name))
        entry_profit.bind("<KeyRelease>", lambda event: on_profit(event, entry=entry_profit))
        db_values()
        table_recipe2ingredient_insert()


class ingredientsRoot(Section):
    """PANTALLA DE INGREDIENTES CON SUS FUNCIONALIDADES"""

    def __init__(self):
        super().__init__()

    def show(self):
        # CONFIGURACION
        self.root_config()
        root.title("PH ABM - Materia Prima")

        # ENTRY Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table["columns"] = ("id",
                                 "name",
                                 "price",
                                 "type",
                                 "details",
                                 "delete")

        def table_ingredient_config():
            self.table.column("#0", width=0, stretch=NO)
            self.table.column("id", width=40, anchor=CENTER)
            self.table.column("name", anchor=CENTER)
            self.table.column("price", width=120, anchor=CENTER)
            self.table.column("type", width=100, anchor=CENTER)
            self.table.column("details", width=16, anchor=CENTER)
            self.table.column("delete", width=16, anchor=CENTER)
            self.table.heading("id", text="ID", anchor=CENTER)
            self.table.heading("name", text="Materia Prima", anchor=CENTER)
            self.table.heading("price", text="Costo", anchor=CENTER)
            self.table.heading("type", text="Medida", anchor=CENTER)

        table_ingredient_config()
        entry_id.config(validate="key", validatecommand=(root.register(
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
        self.root_config()
        root.title("PH ABM - Material de Empaque")

        # ENTRYS Y BOTONES
        global photo
        logo_frame = Frame(root, bg="white")
        logo_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        Label(logo_frame, image=photo).pack(expand=YES, anchor="nw")

        self.table = ttk.Treeview(root)
        self.table["columns"] = ("id",
                                 "name",
                                 "cost",
                                 "profit",
                                 "details",
                                 "delete")

        def table_packaging_config():
            self.table.column("#0", width=0, stretch=NO)
            self.table.column("id", width=40, anchor=CENTER)
            self.table.column("name", anchor=CENTER)
            self.table.column("cost", width=120, anchor=CENTER)
            self.table.column("profit", width=100, anchor=CENTER)
            self.table.column("details", width=16, anchor=CENTER)
            self.table.column("delete", width=16, anchor=CENTER)
            self.table.heading("id", text="ID", anchor=CENTER)
            self.table.heading("name", text="Material de Empaque", anchor=CENTER)
            self.table.heading("cost", text="Costo", anchor=CENTER)
            self.table.heading("profit", text="Beneficio", anchor=CENTER)

        table_packaging_config()
        entry_id.config(validate="key", validatecommand=(root.register(
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


main_section = mainRoot()
# main_section.show()
recipes_section = recipesRoot()
ingredients_section = ingredientsRoot()
packagings_section = packagingsRoot()
if __name__ == "__main__":
    recipes_section.details_recipe(DBM.query_get_recipe("Alfajores"))
    pass

root.mainloop()
