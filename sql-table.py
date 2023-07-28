from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import orm

engine = create_engine('sqlite:///ph_database.db')
Base = orm.declarative_base()


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
    def __init__(self, session: orm.session.Session):
        self.session = session

    def add_recipe(self, recipe_name: str, its_ingredients: list):
        """Creamos una receta nueva este debe entregar una lista de ingredientes tipo tupla,
         uno su nombre y en la otra su cantidad"""
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        if not recipe:  # Entra si no existe recipe
            new_recipe = Recipes(name=recipe_name.capitalize())
            self.session.add(new_recipe)
            for ingredient_name, amount in its_ingredients:
                ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
                if ingredient:
                    ingredient2recipe = RecipeIngredients(recipe_id=new_recipe.id, ingredient_id=ingredient.id,
                                                          amount=amount)
                    self.session.add(ingredient2recipe)
            self.session.commit()

    def delete_recipe(self, recipe_name: str):
        """Elimina una receta por completo y toda su relacion"""
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()

        self.session.delete(recipe)
        self.session.commit()

    def add_rw2recipe(self, recipe_name: str, ingredient_name: str, amount: float):
        """Añade un ingrediente a una receta"""
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id,
                                                                            ingredient_id=ingredient.id).first()

        if not ingredient2recipe:  # Entra si no existe ingredient2recipe
            ingredient2recipe = RecipeIngredients(recipe_id=recipe.id, ingredient_id=ingredient.id, amount=amount)
            self.session.add(ingredient2recipe)
            self.session.commit()

    def modify_rw2recipe(self, recipe_name: str, ingredient_name: str, amount: float):
        """Modifica la cantidad necesaria de un ingrediente en la receta"""
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id,
                                                                            ingredient_id=ingredient.id).first()

        if ingredient2recipe:  # Entra si existe ingrediente2recipe
            ingredient2recipe.amount = amount
            self.session.commit()

    def remove_rw2recipe(self, recipe_name: str, ingredient_name: str):
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id,
                                                                            ingredient_id=ingredient.id).first()

        self.session.delete(ingredient2recipe)
        self.session.commit()

    def add_ingredient(self, ingredient_name: str, ingredient_price: int, ingredient_unitype: str = None):
        ingredient_exist = self.session.query(Ingredients).filter_by(name=ingredient_name).first()
        if not ingredient_exist:
            ingredient = Ingredients(name=ingredient_name.capitalize(), price=ingredient_price)

            if ingredient_unitype:
                ingredient.unit_type = ingredient_unitype.upper()

            self.session.add(ingredient)
            self.session.commit()

    def modify_price(self, ingredient_name: str, new_price: float):
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()

        if ingredient and new_price > 0:
            ingredient.price = new_price

        self.session.commit()

    def delete_ingredient(self, ingredient_name: str):
        ingredients = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).all()
        for ingredient in ingredients:
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

    dbm.session.query(Ingredients).delete()
    dbm.add_ingredient("azucar", 585)
    dbm.add_ingredient("cacao amargo", 7800)
    dbm.add_ingredient("cebolla", 180)
    dbm.add_ingredient("albaca", 40, "unidad")
    dbm.add_ingredient("Harina 000", 175)
    dbm.add_ingredient("Harina 0000", 246)

    ingredients = dbm.session.query(Ingredients).all()
    print(f"| {'id'.ljust(3)} |  {'nombre'.ljust(20)} | {'precio'.ljust(8)} | {'u m'.ljust(6)} |")
    for ingredient in ingredients:
        id_str = str("{:03d}".format(ingredient.id)).ljust(2)
        name_str = ingredient.name.ljust(20)
        price_str = str(ingredient.price).ljust(8)
        unit_type_str = str(ingredient.unit_type).ljust(6)
        print(f"| {id_str} |  {name_str} | {price_str} | {unit_type_str} |")

    dbm.session.query(Recipes).delete()
    dbm.add_recipe("tarta", [("azucar", 0.2), ("pepino", 0.5), ("harina 000", 1)])
    dbm.add_recipe("tarta", [("azucar", 0.2), ("pepino", 0.5), ("harina 000", 1)])

    recipes = dbm.session.query(Recipes).all()
    for recipe in recipes:
        print(recipe.name, end=" >> ")
        for ingredient in recipe.ingredients:
            print(ingredient.ingredient.name, end=", ")
        print("\n")


if __name__ == "__main__":
    main()
