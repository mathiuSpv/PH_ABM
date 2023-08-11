from tkinter import *
from tkinter import Tk, ttk, messagebox
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
        table_frame = Frame(self.master, bg="white")
        table_frame.grid(row=3, column=2, sticky="nsew", rowspan=2)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        def load_table_from_recipes():
            table = ttk.Treeview(table_frame)
            table['columns'] = ('id',
                                'name',
                                'price',
                                'units',
                                'details',
                                'delete')

            def __on_table_click__(event):
                col = table.identify_column(event.x)
                recipe_id = table.item(table.selection()[0], 'values')[0]
                recipe_name = table.item(table.selection()[0], 'values')[1]
                match col:
                    case '#5':
                        """Detalles de la receta"""
                        recipe_details = DBM.query_get_recipe(recipe_name)
                        self.details_top = Toplevel(self.master)
                        self.details_top.title("Detalles de la receta")
                        self.details_top.iconbitmap("ph_icon.ico")
                        self.details_top.config(bg="white")
                        self.__set_toplevel__()
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
                                                     P.isdigit() and len(P) <= 5) else False), "%P"),
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
                        Label(self.details_top, text=f"COSTO TOTAL $ {recipe_details.total_cost()}",
                              bg="white").grid(row=2, column=1, sticky="se")

                        # === Label Beneficio
                        Label(self.details_top, text="X BENEFICIO",
                              bg="white").grid(row=3, column=1, sticky="ne", padx=50)
                        entry_profit = Entry(self.details_top,
                                             validate="key",
                                             validatecommand=(self.details_top.register(
                                                 lambda P: True if P == "" or len(P) <= 3 else False), "%P"),
                                             width=4)
                        entry_profit.insert(0, recipe_details.profit)
                        entry_profit.grid(row=3, column=1, sticky="ne", padx=12)

                        def __profit_price__(profit: float):
                            profit_msg = f"        BENEFICIO $ {round(profit, 2)}"
                            if recipe_details.units != 1:
                                profit_cu = round(
                                    (recipe_details.total_cost() * recipe_details.profit) / recipe_details.units, 2)
                                profit_cu_msg = f"\nBENEFICIO C/U $ {profit_cu}"
                            else:
                                profit_cu_msg = ""
                            return str(profit) + profit_cu_msg

                        profit_total = Label(self.details_top,
                                             text=f"        BENEFICIO $ {__profit_price__}",
                                             bg="white")
                        profit_total.grid(row=3, column=2, sticky="nw")

                        def __on_key__(event):
                            content = entry_profit.get()
                            try:
                                if content[1].isnumeric():
                                    entry_profit.delete(0, END)
                                    entry_profit.insert(0, f"{content[0]}.{content[1]}")
                                elif content[1] != ".":
                                    entry_profit.delete(0, END)
                                    entry_profit.insert(0, f"{content[0]}.0")
                                profit = float(content)
                            except IndexError:
                                if not content:
                                    profit =
                                elif content[0].isnumeric():
                                    profit = float(content[0])

                            except Exception as e:
                                profit = recipe_details.profit
                                print(type(e).__name__)
                            finally:
                                if profit:
                                    profit_ = round(recipe_details.total_cost() * profit_, 2)
                                    profit_total.config(text=f"BENEFICIO $ {profit_}")

                        entry_profit.bind("<KeyRelease>", __on_key__)

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

                        table_ingredients2recipe = ttk.Treeview(self.details_top)
                        table_ingredients2recipe['columns'] = ('id',
                                                               'name',
                                                               'quantity')
                        table_ingredients2recipe.column('#0', width=0, stretch=NO)
                        table_ingredients2recipe.column('id', width=40, anchor=CENTER)
                        table_ingredients2recipe.column('name', width=140, anchor=CENTER)
                        table_ingredients2recipe.column('quantity', width=80, anchor=CENTER)
                        table_ingredients2recipe.heading("id", text="ID")
                        table_ingredients2recipe.heading("name", text="Nombre")
                        table_ingredients2recipe.heading("quantity", text="Cantidad")
                        ingredients2recipe = DBM.query_get_ingredients2recipe(recipe_details.name)
                        for ingredient, ingredient_amount in ingredients2recipe:
                            ingredient_row = [ingredient.id, ingredient.name,
                                              f"{ingredient_amount}{ingredient.unit_type}"]
                            table_ingredients2recipe.insert(parent='', index='end', values=ingredient_row)

                        table_ingredients2recipe.grid(row=2, column=1, sticky="w", columnspan=2)

                    case '#6':
                        """Eliminar la fila receta"""
                        answer = messagebox.askyesno(
                            title="Eliminar",
                            message="ELIMINAR DE RECETAS:\n"
                                    f"ID {recipe_id} : {recipe_name}")
                        if answer:
                            DBM.del_recipe(recipe_name)
                        load_table_from_recipes()
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

        load_table_from_recipes()

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

    def __set_toplevel__(self, geometry_size: str = "380x380"):
        window_width = self.details_top.winfo_reqwidth()
        window_height = self.details_top.winfo_reqheight()
        position_t_right = int(position_right + (window_height / 1))
        position_t_down = int(position_down + (window_width / 2))
        self.details_top.geometry(f'{geometry_size}' + '+{}+{}'.format(position_t_right, position_t_down))
        self.details_top.resizable(False, False)
        self.details_top.grab_set()


def main():
    MiApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
