from tkinter import *
from tkinter import Tk, ttk, messagebox
from PIL import Image, ImageTk
from sql_ph import DBM

root = Tk()
position_right = int((root.winfo_screenwidth() * (1 / 5)))
position_down = int((root.winfo_screenheight() * (1 / 5)))
standar_position = "+{}+{}".format(position_right, position_down)
photo = None


def __update_treeview__(tree: ttk.Treeview, data):
    for row in tree.get_children():
        tree.delete(row)

    for item in data:
        tree.insert("", 'end', values=item)


def __refractor_row__(*args):
    return args


def __set_middle__(windows_object, geometry_size: str = "380x380", padx: int = 0, pady: int = 0):
    window_width = windows_object.winfo_reqwidth()
    window_height = windows_object.winfo_reqheight()
    position_t_right = int(position_right + (window_height / 1))
    position_t_down = int(position_down + (window_width / 2))
    windows_object.geometry(f'{geometry_size}' + '+{}+{}'.format(padx + position_t_right,
                                                                 pady + position_t_down))
    windows_object.resizable(False, False)
    windows_object.grab_set()


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
        self.master.geometry('480x320' + standar_position)
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
        table_recipe = ttk.Treeview(self.master)
        table_recipe['columns'] = ('id',
                                   'name',
                                   'price',
                                   'units',
                                   'details',
                                   'delete')
        table_recipe.column('#0', width=0, stretch=NO)
        table_recipe.column('id', width=40, anchor=CENTER)
        table_recipe.column('name', anchor=CENTER)
        table_recipe.column('price', width=100, anchor=CENTER)
        table_recipe.column('units', width=100, anchor=CENTER)
        table_recipe.column('details', width=12, anchor=CENTER)
        table_recipe.column('delete', width=12, anchor=CENTER)
        table_recipe.heading('id', text="ID", anchor=CENTER)
        table_recipe.heading('name', text="Receta", anchor=CENTER)
        table_recipe.heading('price', text="Precio C/U", anchor=CENTER)
        table_recipe.heading('units', text="Cantidad", anchor=CENTER)
        table_recipe.grid(row=3, column=2, sticky="nsew", rowspan=2)

        def __recipe_table__():
            for row in table_recipe.get_children():
                table_recipe.delete(row)

            recipes = DBM.query_get_all_recipes()
            for recipe in recipes:
                recipe_row = __refractor_row__(recipe.id, recipe.name,
                                               recipe.price_for_unit(), recipe.units,
                                               "📝", " 🗑️")
                table_recipe.insert("", "end", values=recipe_row)

        def __on_table_click__(event):
            try:
                col = table_recipe.identify_column(event.x)
                recipe_id = table_recipe.item(table_recipe.selection()[0], 'values')[0]
                recipe_name = table_recipe.item(table_recipe.selection()[0], 'values')[1]
                match col:
                    case '#6':
                        """Eliminar la fila receta"""
                        answer = messagebox.askyesno(
                            title="Eliminar Receta",
                            message="Eliminar Receta:\n"
                                    f"ID {recipe_id} : {recipe_name}")
                        if answer:
                            DBM.del_recipe(recipe_name)
                            __recipe_table__()
                    case _:
                        """Detalles de la receta"""
                        self.details_for_recipe(recipe_name)
            except IndexError:
                pass

        __recipe_table__()
        table_recipe.bind('<ButtonRelease-1>', __on_table_click__)

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

    def details_for_recipe(self, recipe_name):
        recipe_details = DBM.query_get_recipe(recipe_name)
        self.details_top = Toplevel(self.master)
        self.details_top.title("Detalles de la receta")
        self.details_top.iconbitmap("ph_icon.ico")
        self.details_top.config(bg="white")
        __set_middle__(self.details_top)
        self.details_top.rowconfigure(0, minsize=12)  # Espacios
        self.details_top.rowconfigure(1, minsize=54)
        self.details_top.rowconfigure(2, weight=12)
        self.details_top.rowconfigure(3, weight=3)
        self.details_top.rowconfigure(5, minsize=2)  # Espacios
        self.details_top.columnconfigure(0, minsize=12)  # Espacios
        self.details_top.columnconfigure(1, minsize=80)
        self.details_top.columnconfigure(2, weight=3)
        self.details_top.columnconfigure(3, weight=1)
        self.details_top.columnconfigure(4, minsize=12)  # Espacios

        # === Label de ID receta
        Label(self.details_top, text=" ID ", bg="white").grid(
            row=1, column=1, sticky="nw")
        entry_id = Entry(self.details_top,
                         validate="key",
                         validatecommand=(self.details_top.register(
                             lambda P: True if P == "" or (
                                     P.isdigit() and len(P) <= 3) else False), "%P"),
                         width=4)
        entry_id.insert(0, f"{recipe_details.id}")
        entry_id.grid(row=1, column=1, sticky="w")

        # === Label de Nombre de la receta
        Label(self.details_top, text="   NOMBRE ", bg="white").grid(
            row=1, column=1, sticky="ne", padx=38)
        entry_name = Entry(self.details_top,
                           validate="key",
                           validatecommand=(self.details_top.register(
                               lambda P: True if P == "" or len(P) <= 16 else False), "%P"),
                           width=16)
        entry_name.insert(0, f"{recipe_details.name}")
        entry_name.grid(row=1, column=1, sticky="e", padx=16)

        # === Label Ingredientes de la receta
        Label(self.details_top, text="INGREDIENTES DE LA RECETA ", bg="white").grid(
            row=2, column=1, sticky="ne")

        # === Label Costo Total
        label_total_cost = Label(self.details_top,
                                 bg="white")
        label_total_cost.grid(row=2, column=1, sticky="se")

        # === Label Beneficio
        Label(self.details_top, text="X BENEFICIO",
              bg="white").grid(row=3, column=1, sticky="ne", padx=50)
        entry_profit = Entry(self.details_top,
                             validate="key",
                             validatecommand=(self.details_top.register(
                                 lambda P: True if P == "" or (
                                         P[0].isnumeric() and len(P) <= 3) else False), "%P"),
                             width=4)
        entry_profit.insert(0, recipe_details.profit)
        entry_profit.grid(row=3, column=1, sticky="ne", padx=12)

        # === Label Beneficios $
        def __profit_price__():
            try:
                profit = float(entry_profit.get())
            except ValueError:
                profit = recipe_details.profit
            except Exception as e:
                print(type(e).__name__)
                profit = recipe_details.profit
            profit_msg = f"         BENEFICIO $ {round(recipe_details.total_cost() * profit, 1)}"
            if recipe_details.units != 1:
                profit_cu = round(
                    (recipe_details.total_cost() * profit) / recipe_details.units, 1)
                profit_cu_msg = f"\nBENEFICIO C/U $ {profit_cu}"
            else:
                profit_cu_msg = ""
            return profit_msg + profit_cu_msg

        profit_label = Label(self.details_top,
                             text=f"{__profit_price__()}",
                             bg="white")
        profit_label.grid(row=3, column=2, columnspan=2, sticky="nw")

        def __on_key_profit__(event):
            content = entry_profit.get()
            if event.keysym.isnumeric():
                match len(content):
                    case 3:
                        entry_profit.delete(0, END)
                        entry_profit.insert(0, f"{content[0]}.{event.keysym}")
                    case 2:
                        entry_profit.delete(0, END)
                        entry_profit.insert(0, f"{content[0]}.{event.keysym}")
                    case 1:
                        entry_profit.delete(0, END)
                        entry_profit.insert(0, f"{content[0]}.")
            elif event.keysym == "BackSpace":
                match len(content):
                    case 2:
                        entry_profit.delete(0, END)
                        entry_profit.insert(0, f"{content[0]}")
                    case 1:
                        entry_profit.delete(0, END)
            profit_label.config(text=__profit_price__())

        entry_profit.bind("<KeyRelease>", __on_key_profit__)

        # === Label unidades
        Label(self.details_top, text="UNIDADES", bg="white").grid(
            row=1, column=2, sticky="nw")
        entry_units = Entry(self.details_top,
                            validate="key",
                            validatecommand=(self.details_top.register(
                                lambda P: True if P == "" or (
                                        P.isdigit() and len(P) <= 2) else False), "%P"),
                            width=3)
        entry_units.insert(0, f"{recipe_details.units}")
        entry_units.grid(row=1, column=2, sticky="w", padx=20)

        # TABLE INGREDIENT2RECIPE
        table_ingredients2recipe = ttk.Treeview(self.details_top)
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
        table_ingredients2recipe.heading("name", text="Nombre")
        table_ingredients2recipe.heading("quantity", text="Cantidad")
        table_ingredients2recipe.grid(row=2, column=1, sticky="w", columnspan=2)

        def __ingredient2recipe_table__():
            for row in table_ingredients2recipe.get_children():
                table_ingredients2recipe.delete(row)

            ingredients2recipe = DBM.query_get_all_ingredients2recipe(recipe_details.name)
            for ingredient, ingredient_amount in ingredients2recipe:
                ingredient_row = __refractor_row__(ingredient.id, ingredient.name,
                                                   f"{ingredient_amount}{ingredient.unit_type}",
                                                   "📝", " 🗑️")
                table_ingredients2recipe.insert(parent='', index='end', values=ingredient_row)
            label_total_cost.config(text=f"COSTO TOTAL $ {recipe_details.total_cost()}")
            profit_label.config(text=__profit_price__())

        def __on_table_click__(event):
            try:
                col = table_ingredients2recipe.identify_column(event.x)
                ingredient_id = table_ingredients2recipe.item(
                    table_ingredients2recipe.selection()[0], 'values')[0]
                ingredient_name = table_ingredients2recipe.item(
                    table_ingredients2recipe.selection()[0], 'values')[1]
                match col:
                        case '#4':
                            """Detalles de la receta"""
                            def __on_key_amount__(event):
                                content = entry_value.get()
                                if event.keysym.isnumeric():
                                    match len(content):
                                        case 2:
                                            entry_value.delete(0, END)
                                            entry_value.insert(0, f"{content}.")
                                        case 4:
                                            print(content[:3:])
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

                            def __func_button_confirm__():
                                try:
                                    amount = float(entry_value.get())
                                    DBM.mdf_amount_ingredient2recipe(recipe_name, ingredient_name, amount)
                                    response.destroy()
                                    __ingredient2recipe_table__()
                                except ValueError:
                                    pass
                                except Exception as e:
                                    print(type(e).__name__)
                                    pass

                            response = Toplevel(self.details_top)
                            response.title("")
                            response.iconbitmap('ph_icon.ico')
                            __set_middle__(response, geometry_size="180x105", padx=100, pady=40)
                            response.rowconfigure(0, weight=5)
                            response.rowconfigure(1, weight=2)
                            response.columnconfigure(0, weight=2)
                            Label(response,
                                  text=f" Modificar cantidad de \n   {ingredient_name} en {recipe_name}").grid(
                                row=0, column=0, sticky="n", pady=2)
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
                        case '#5':
                            """Eliminar la fila ingrediente de la receta"""
                            answer = messagebox.askyesno(
                                title="Eliminar Ingrediente de la Receta",
                                message="Esta Seguro de Eliminar :\n"
                                        f"ID {ingredient_id} : {ingredient_name} de {recipe_name}")
                            if answer:
                                DBM.remove_ingredient2recipe(recipe_name, ingredient_name)
                                __ingredient2recipe_table__()
            except IndexError:
                pass

        __ingredient2recipe_table__()
        table_ingredients2recipe.bind('<ButtonRelease-1>', __on_table_click__)

        Button(self.details_top, text="Guardar", bg="white").grid(row=1, column=3)
        Button(self.details_top, text="Previo", bg="white").grid(row=2, column=3, sticky="n")


def main():
    MiApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
