from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import orm

engine = create_engine('sqlite:///ph_database.db')
Base = orm.declarative_base()
ID= 0
NAME= 1
PRICE= 2

class RecipeIngredients(Base):
    """Crear una tabla que contenga la union de las dos tablas"""
    __tablename__ = 'ingredients2recipes'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    amount = Column(Float, nullable=False, default=1.00)

    """Relacion unidireccional de RecipeIngredients > Ingredients y
    bidireccional con Recipe > RecipeIngredients"""
    recipe = relationship("Recipes", back_populates="ingredients")
    ingredient = relationship("Ingredients")


class Recipes(Base):
    """Creacion de la tabla de Recetas, esta tiene una relacion con la tabla recipe_rawm_association,
    de esta forma se relaciona de forma directa con todos los ingredientes requeridos"""
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    "Relacion bidireccional de Recipes > RecipeIngredients"
    ingredients = relationship("RecipeIngredients", back_populates="recipe",
                               cascade="all, delete")


class Ingredients(Base):
    """Creacion de la tabla de Materia Prima"""
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit_type = Column(String, nullable=False, default="KG")  # Existen (unidad, kg, litro)


class DBManager:
    def __init__(self, session_local: orm.session.Session):
        self.session = session_local

    def query_get_recipe(self, recipe_name: str):
        """Retorna el elemento de la tabla Recipes"""
        try:
            recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
            if recipe:
                return recipe
            return False
        except Exception as e:
            return False

    def query_get_ingredient(self, ingredient_name: str):
        """Retorna el elemento de la tabla Ingredients"""
        try:
            ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
            if ingredient:
                return ingredient
            return False
        except Exception as e:
            return False

    def query_get_rw2recipe(self, recipe_name: str, ingredient_name: str, return_as_bucket: bool = False):
        """Retorna un elemento de la tabla RecipeIngredients, puede retornar tambien sus elementos Recipe y Ingredients
        con el parametro return_as_bucket"""
        try:
            recipe = self.query_get_recipe(recipe_name)
            ingredient = self.query_get_ingredient(ingredient_name)
            if recipe and ingredient:
                recipe_ingredient = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id,
                                                                                    ingredient_id=ingredient.id).first()
            if recipe_ingredient:
                if return_as_bucket:
                    return recipe, ingredient, recipe_ingredient
                return recipe_ingredient
            raise Exception
        except Exception as e:
            if return_as_bucket:
                return recipe, ingredient, False
            return False

    def query_all_recipes(self):
        recipes = self.session.query(Recipes).all()
        all_recipes = [(recipe.id,recipe.name,recipe.price) for recipe in recipes]
        return all_recipes

    def query_all_ingredients(self):
        ingredients = self.session.query(Ingredients).all()
        all_ingredients = [(ingredient.id, ingredient.name, ingredient.price) for ingredient in ingredients]
        return all_ingredients

    def query_all_rw2recipes(self):
        return self.session.query(RecipeIngredients).all()

    def add_recipe(self, recipe_name: str, recipe_price: float, its_ingredients: list):
        """Creamos una receta nueva este debe entregar una lista de ingredientes tipo tupla,
         uno su nombre y en la otra su cantidad"""
        if not self.query_get_recipe(recipe_name):# Entra si no existe recipe
            recipe = Recipes(name=recipe_name.capitalize(), price=recipe_price)
            self.session.add(recipe)
            self.session.commit()
            for ingredient_name, amount in its_ingredients:
                self.add_rw2recipe(recipe_name, ingredient_name, amount)

    def delete_recipe(self, recipe_name: str):
        """Elimina una receta por completo y toda su relacion"""
        recipe = self.query_get_recipe(recipe_name)

        if recipe:
            self.session.delete(recipe)
            self.session.commit()

    def add_rw2recipe(self, recipe_name: str, ingredient_name: str, amount: float):
        """Añade un ingrediente a una receta"""
        recipe, ingredient, ingredient2recipe = self.query_get_rw2recipe(recipe_name, ingredient_name,
                                                                         return_as_bucket=True)
        if recipe and ingredient and not ingredient2recipe: #Entra si no existe ingredient2recipe
            ingredient2recipe = RecipeIngredients(recipe_id=recipe.id, ingredient_id=ingredient.id)
            ingredient2recipe.amount = amount if isinstance(amount, float) and amount > 0 else None
            self.session.add(ingredient2recipe)
            self.session.commit()

    def modify_rw2recipe(self, recipe_name: str, ingredient_name: str, amount: float):
        """Modifica la cantidad necesaria de un ingrediente en la receta"""
        ingredient2recipe = self.query_get_rw2recipe(recipe_name, ingredient_name)

        if ingredient2recipe:  # Entra si existe ingrediente2recipe
            ingredient2recipe.amount = amount if isinstance(amount, float) and amount > 0 else None
            self.session.commit()

    def remove_rw2recipe(self, recipe_name: str, ingredient_name: str):
        ingredient2recipe = self.query_get_rw2recipe(recipe_name, ingredient_name)

        if ingredient2recipe:
            self.session.delete(ingredient2recipe)
            self.session.commit()

    def add_ingredient(self, ingredient_name: str, ingredient_price: int, ingredient_unitype: str = None):
        ingredient = self.query_get_ingredient(ingredient_name)

        if not ingredient:
            ingredient = Ingredients(name=ingredient_name.capitalize(), price=ingredient_price)

            ingredient.unit_type = ingredient_unitype.upper() if isinstance(ingredient_unitype, str) else None
            ingredient.id = 101 if len(self.query_all_ingredients()) == 0 else None

            self.session.add(ingredient)
            self.session.commit()

    def modify_id(self, ingredient_name: str, new_id: int):
        ingredient = self.query_get_ingredient(ingredient_name)

        if ingredient:
            ingredient.id = new_id if isinstance(new_id, int) and ingredient.id > 0 else ingredient.id
            self.session.commit()

    def modify_price(self, ingredient_name: str, new_price: float):
        ingredient = self.query_get_ingredient(ingredient_name)

        if ingredient:
            ingredient.price = new_price if isinstance(new_price, float) and new_price > 0 else ingredient.id
            self.session.commit()

    def delete_ingredient(self, ingredient_name: str):
        ingredient = self.query_get_ingredient(ingredient_name)

        if ingredient:
            self.session.delete(ingredient)
            self.session.commit()


"""Creacion y relacion con toda la DB"""
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
dbm = DBManager(session)


def main():
    """Testing del la DB"""
    print(f"{dbm.session.bind.url} conectada!")
    # for tables in Base.metadata.tables:
    #     print(tables)

    dbm.add_ingredient("azucar", 585)
    dbm.add_ingredient("cacao amargo", 7800)
    dbm.add_ingredient("cebolla", 180)
    dbm.add_ingredient("albaca", 40, "unidad")
    dbm.add_ingredient("Harina 000", 175)
    dbm.add_ingredient("Harina 0000", 246)
    dbm.modify_id("cebolla", 230)
    ingredients = dbm.session.query(Ingredients).all()

    print(f"| {'id'.ljust(3)} |  {'nombre'.ljust(20)} | {'precio'.ljust(8)} | {'u m'.ljust(6)} |")
    for ingredient in ingredients:
        id_str = str("{:03d}".format(ingredient.id)).ljust(2)
        name_str = ingredient.name.ljust(20)
        price_str = str(ingredient.price).ljust(8)
        unit_type_str = str(ingredient.unit_type).ljust(6)
        print(f"| {id_str} |  {name_str} | {price_str} | {unit_type_str} |")
        
    dbm.add_recipe("tarta", 720, [("azucar", 0.2), ("pepino", 0.5), ("harina 000", 3.0)])
    dbm.add_recipe("tarta", 720, [("azucar", 0.2), ("pepino", 0.5), ("harina 000", 3)])

    recipes = dbm.session.query(Recipes).all()
    for recipe in recipes:
        print(recipe.name, end=" >> ")
        for ingredient in recipe.ingredients:
            print(ingredient.ingredient.name, ingredient.amount, end=", ")
        print("\n")



if __name__ == "__main__":
    main()
