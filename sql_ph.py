from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import orm

engine = create_engine('sqlite:///ph_database.db')
Base = orm.declarative_base()

"""La Base de Datos se definen dos tipos de tabla:
Tabla Principal: Contiene escencialmente los nombres de los productos y su precio
Tabla Relacional: Contiene las id conectoras de dos tablas y tiene la cantidad que se tiene con las dos tablas"""
ID, NAME, PRICE = 0, 1, 2  # Constantes: Utilizar solo en Tablas Principales


class RecipeIngredients(Base):
    """Creacion de una tabla que contenga la union de Recipes y Ingredients
    def: Tabla Relacional"""
    __tablename__ = 'ingredients2recipes'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    amount = Column(Float, nullable=False, default=1.00)

    """Relacion unidireccional de RecipeIngredients > Ingredients y
    bidireccional con Recipe > RecipeIngredients"""
    recipe = relationship("Recipes", back_populates="ingredients")
    ingredient = relationship("Ingredients")


class RecipePackagings(Base):
    """Creacion de una tabla que contenga la union de Recipes y Packagings
    def: Tabla Relacional"""
    __tablename__ = 'packaging2recipe'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    packaging_id = Column(Integer, ForeignKey('packagings.id'), nullable=False)
    amount = Column(Integer, nullable=False)

    """Relacion unidireccional de RecipePackagings > Packagings y
    bidireccional con Recipe > RecipePackagings"""
    recipe = relationship("Recipes", back_populates="packagings")
    packaging = relationship("Packagings")


class Recipes(Base):
    """Creacion de la tabla de Recetas, esta tiene una relacion con la Tabla Ingredients & Packagings
    def: Tabla Principal"""
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)

    """Relacion bidireccional de Recipes > RecipeIngredients
    Relacion bidireccional de Recipes > RecipePackagings"""
    ingredients = relationship("RecipeIngredients", back_populates="recipe",
                               cascade="all, delete")
    packagings = relationship("RecipePackagings", back_populates="recipe",
                              cascade="all, delete")


class Ingredients(Base):
    """Creacion de la tabla de Materia Prima
    def: Tabla Principal"""
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit_type = Column(String, nullable=False)  # Existen (unidad, kg, litro)


class Packagings(Base):
    """Creacion de la tabla de Material de Empaque
    def: Tabla Principal"""
    __table__ = 'packagings'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(Integer, nullable=False)


def __capitalize__(*args_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs = {k: v.capitalize() if k in args_name and isinstance(v, str) else v for k, v in kwargs.items()}
            return func(*args, **kwargs)

        return wrapper

    return decorator


class DBManager:
    """DB Manager para poder controlar todas las herramientas que se van a utilizar en la DB
    Cabe declarar que las funciones pueden estar hechas para Tablas Principales y Relacionales.
    Leer en Linea 10 la diferencia."""

    def __init__(self, session_local: orm.session.Session):
        self.session = session_local

    """Todas las Querys disponibles hacia Tablas Pricipales"""

    @__capitalize__('recipe_name')
    def qry_get_recipe(self, recipe_name: str, everything: bool = False):
        try:
            if everything:
                query_recipes = self.session.query(Recipes).filter(
                    Recipes.name.like(f'%{recipe_name}%')).all()
                return [(recipe.id, recipe.name, recipe.price) for recipe in query_recipes]
            query_recipe = self.session.query(Recipes).filter(
                Recipes.name.like(f'%{recipe_name}%')).first()
            return query_recipe.id, query_recipe.name, query_recipe.price
        except AttributeError:
            return False
        except Exception as e:
            print(type(e).__name__, e)
            return False

    @__capitalize__('ingredient_name')
    def qry_get_ingredient(self, ingredient_name: str, everything: bool = False):
        try:
            if everything:
                query_ingredients = self.session.query(Ingredients).filter(
                    Ingredients.name.like(f'%{ingredient_name}%')).all()
                return [(ingredient.id, ingredient.name, ingredient.price) for ingredient in query_ingredients]
            ingredient = self.session.query(Ingredients).filter(
                Ingredients.name.like(f'%{ingredient_name}%')).first()
            return ingredient.id, ingredient.name, ingredient.price
        except AttributeError:
            return False
        except Exception as e:
            print(type(e).__name__, e)
            return False

    @__capitalize__('packaging_name')
    def qry_get_packaging(self, packaging_name: str, everything: bool = False):
        try:
            if everything:
                query_packagings = self.session.query(Packagings).filter(
                    Packagings.name.like(f'%{packaging_name}%')).all()
                return [(packaging.id, packaging.name, packaging.price) for packaging in query_packagings]
            packaging = self.session.query(Packagings).filter(
                Packagings.name.like(f'%{packaging_name}%')).first()
            return packaging.id, packaging.name, packaging.price
        except AttributeError:
            return False
        except Exception as e:
            print(type(e).__name__, e)
            return False

    def qry_get_all_recipes(self):
        all_recipes = self.session.query(Recipes).all()
        return [(recipe.id, recipe.name, recipe.price) for recipe in all_recipes]

    def qry_get_all_ingredients(self):
        all_ingredients = self.session.query(Ingredients).all()
        return [(ingredient.id, ingredient.name, ingredient.price) for ingredient in all_ingredients]

    def qry_get_all_packagings(self):
        all_packagings = self.session.query(Packagings).all()
        return [(packaging.id, packaging.name, packaging.price) for packaging in all_packagings]

    """Todas las funciones añadir a Tablas Principales:
    Estas funciones retornaran Type: bool"""

    @__capitalize__('recipe_name')
    def add_recipe(self,
                   recipe_id: int,
                   recipe_name: str,
                   cost_price: float,
                   ingredients_: list,
                   packagings_: list,
                   recipe_profit: float = 3
                   ) -> bool:
        recipe_exist = self.qry_get_recipe(recipe_name)
        if not recipe_exist:
            recipe = Recipes(id=recipe_id,
                             name=recipe_name,
                             price=cost_price * recipe_profit,
                             profit=recipe_profit)
            self.session.add(recipe)
            self.session.commit()
            for ingredient_id, ingredient_amount in ingredients_:
                "Añadir la funcion para agregar a Tabla Relacional"
                pass
            for packagings_id, packagings_amount in packagings_:
                "Añadir la funcion para agregar a Tabla Relacional"
                pass

        return not recipe_exist

    @__capitalize__('ingredient_name', 'ingredient_unitype')
    def add_ingredient(self,
                       ingredient_id: int,
                       ingredient_name: str,
                       ingredient_price: float,
                       ingredient_unitype: str
                       ) -> bool:
        ingredient_exist = self.qry_get_ingredient(ingredient_name)
        if not ingredient_exist:
            ingredient = Ingredients(id=ingredient_id,
                                     name=ingredient_name,
                                     price=ingredient_price,
                                     unitype=ingredient_unitype)
            self.session.add(ingredient)
            self.session.commit()

        return not ingredient_exist

    @__capitalize__('packaging_name')
    def add_packaging(self,
                      packaging_id: int,
                      packaging_name: str,
                      packaging_price: float,
                      packaging_unit: int
                      ) -> bool:
        packaging_exist = self.qry_get_packaging(packaging_name)
        if not packaging_exist:
            packaging = Packagings(id=packaging_id,
                                   name=packaging_name,
                                   price=packaging_price,
                                   unit=packaging_unit)
            self.session.add(packaging)
            self.session.commit()

        return not packaging_exist


"""Creacion y relacion con toda la DB"""
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
DBM = DBManager(session)


def main():
    """Testing del la DB"""


if __name__ == "__main__":
    main()
