from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
import inspect

engine = create_engine('sqlite:///ph_database.db')
Base = orm.declarative_base()
decorator_executed = False

"""La Base de Datos se definen dos tipos de tabla:
Tabla Principal: Contiene escencialmente los nombres de los productos y su precio
Tabla Relacional: Contiene las id conectoras de dos tablas y tiene la cantidad que se tiene con las dos tablas"""


class IngredientsRecipes(Base):
    """Creacion de una tabla que contenga la union de Recipes y Ingredients
    def: Tabla Relacional"""
    __tablename__ = 'ingredients2recipes'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    amount = Column(Float, nullable=False, default=1.00)

    """Relacion unidireccional de IngredientsRecipes > Ingredients y
    bidireccional con Recipe > IngredientsRecipes"""
    recipe = relationship("Recipes", back_populates="ingredients")
    ingredient = relationship("Ingredients")


class PackagingsRecipes(Base):
    """Creacion de una tabla que contenga la union de Recipes y Packagings
    def: Tabla Relacional"""
    __tablename__ = 'packaging2recipe'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    packaging_id = Column(Integer, ForeignKey('packagings.id'), nullable=False)
    amount = Column(Integer, nullable=False, default=1)

    """Relacion bidireccional de PackagingsRecipes > Packagings y
    bidireccional con Recipe > PackagingsRecipes"""
    recipe = relationship("Recipes", back_populates="packagings")
    packaging = relationship("Packagings")

    def total_price(self=None):
        return self.recipe.price_for_unit() * self.amount + self.packaging.total_price()


class Recipes(Base):
    """Creacion de la tabla de Recetas, esta tiene una relacion con la Tabla Ingredients & Packagings
    def: Tabla Principal"""
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    profit = Column(Float, nullable=False)
    units = Column(Integer, nullable=False, default=1)

    """Relacion unidireccional de Recipes > IngredientsRecipes
    Relacion bidireccional de Recipes > PackagingsRecipes"""
    ingredients = relationship("IngredientsRecipes", back_populates="recipe",
                               cascade="all, delete")
    packagings = relationship("PackagingsRecipes", back_populates="recipe",
                              cascade="all, delete")

    def as_tuple(self=None):
        return self.id, self.name, self.profit, self.units

    def total_cost(self):
        total_cost = 0
        for ingredient_relation in self.ingredients:
            ingredient = ingredient_relation.ingredient
            total_cost += ingredient.cost * ingredient_relation.amount
        return total_cost

    def cost_for_unit(self):
        return (self.total_cost()) / self.units

    def price_for_unit(self):
        return self.cost_for_unit() * self.profit


class Ingredients(Base):
    """Creacion de la tabla de Materia Prima
    def: Tabla Principal"""
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=True)
    unit_type = Column(String, nullable=False)  # Existen (unidad, kg, litro)

    def as_tuple(self=None):
        return self.id, self.name, self.cost, self.unit_type


class Packagings(Base):
    """Creacion de la tabla de Material de Empaque
    def: Tabla Principal"""
    __tablename__ = 'packagings'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)

    def as_tuple(self=None):
        return self.id, self.name, self.cost

    def total_price(self):
        return self.cost * self.profit


def __capitalize__(*args_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_values = sig.bind(*args, **kwargs)
            bound_values.apply_defaults()
            for name in args_name:
                if name in bound_values.arguments and isinstance(bound_values.arguments[name], str):
                    bound_values.arguments[name] = bound_values.arguments[name].capitalize()
            new_args = [bound_values.arguments[param_name] for param_name in
                        bound_values.signature.parameters if
                        bound_values.signature.parameters[param_name].default == inspect.Parameter.empty]
            new_kwargs = {param_name: bound_values.arguments[param_name] for param_name in
                          bound_values.signature.parameters if
                          bound_values.signature.parameters[param_name].default != inspect.Parameter.empty}
            return func(*new_args, **new_kwargs)

        return wrapper

    return decorator


class _DBManager:
    """DB Manager para poder controlar todas las herramientas que se van a utilizar en la DB
    Cabe declarar que las funciones pueden estar hechas para Tablas Principales y Relacionales.
    Leer en Linea 10 la diferencia."""

    def __init__(self, session_local: orm.session.Session):
        self.session = session_local

    def __insert__(self, Object):
        """Funcion privada del objeto DBManager que nos permite omitir los errores
        de asignacion de ID a cada tabla, esto nos permite que a pesar que el usuario
        coloque un valor ya ocupado este se va a fixear solo"""
        try:
            self.session.add(Object)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            Object.id = None
            self.session.add(Object)
            self.session.commit()
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")

    """Todas las Querys disponibles hacia Tablas Pricipales"""

    @__capitalize__('recipe_name')
    def query_get_recipe(self, recipe_name: str, everything: bool = False):
        try:
            if everything:
                result = self.session.query(Recipes).filter(
                    Recipes.name.like(f'%{recipe_name}%')).all()
            else:
                result = self.session.query(Recipes).filter_by(
                    name=recipe_name).first()
            return result if result else False
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")
            return False

    @__capitalize__('ingredient_name')
    def query_get_ingredient(self, ingredient_name: str, everything: bool = False):
        try:
            if everything:
                result = self.session.query(Ingredients).filter(
                    Ingredients.name.like(f'%{ingredient_name}%')).all()
            else:
                result = self.session.query(Ingredients).filter_by(
                    name=ingredient_name).first()
            return result if result else False
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")
            return False

    @__capitalize__('packaging_name')
    def query_get_packaging(self, packaging_name: str, everything: bool = False):
        try:
            if everything:
                result = self.session.query(Packagings).filter(
                    Packagings.name.like(f'%{packaging_name}%')).all()
            else:
                result = self.session.query(Packagings).filter_by(
                    name=packaging_name).first()
            return result if result else False
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")
            return None

    def query_get_all_recipes(self):
        all_recipes = self.session.query(Recipes).all()
        return [recipe for recipe in all_recipes]

    def query_get_all_ingredients(self):
        all_ingredients = self.session.query(Ingredients).all()
        return [ingredient for ingredient in all_ingredients]

    def query_get_all_packagings(self):
        all_packagings = self.session.query(Packagings).all()
        return [packaging for packaging in all_packagings]

    """Todas las Querys disponibles hacia Tablas Relacionales"""

    def query_get_ingredients2recipe(self, recipe_name: str):
        recipe_exist = self.query_get_recipe(recipe_name)
        if recipe_exist:
            recipe = recipe_exist
            return [(recipe_ingredient.ingredient, recipe_ingredient.amount)
                    for recipe_ingredient in recipe.ingredients]

    def query_get_packaging2recipe(self, recipe_name: str, packaging_name: str, parent_to: bool = False):
        result = []
        packaging2recipe_exist = False
        recipe_exist = self.query_get_recipe(recipe_name)
        packaging_exist = self.query_get_packaging(packaging_name)
        if parent_to:
            result.append(recipe_exist)
            result.append(packaging_exist)
        try:
            recipe, packaging = recipe_exist, packaging_exist
            packaging2recipe_exist = self.session.query(PackagingsRecipes).filter(
                (PackagingsRecipes.recipe_id == recipe.id) & (
                        PackagingsRecipes.packaging_id == packaging.id)).first()
        except AttributeError:
            pass
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")
            pass
        finally:
            result.append(packaging2recipe_exist)
            return tuple(result)

    def query_get_all_packagings2recipe(self, recipe_name: str):
        recipe_exist = self.query_get_recipe(recipe_name)
        if recipe_exist:
            recipe = recipe_exist
            return [recipe_packaging.packaging
                    for recipe_packaging in recipe.packagings]

    """Todas las funciones añadir a Tablas Principales:
    Estas funciones retornaran Type: bool"""

    @__capitalize__('recipe_name')
    def add_recipe(self,
                   recipe_name: str,
                   recipe_profit: float,
                   recipe_units: int,
                   ingredients_: list = None,
                   recipe_id: int = None,
                   ) -> bool:
        recipe_exist = self.query_get_recipe(recipe_name)
        if not recipe_exist:
            recipe = Recipes(id=recipe_id,
                             name=recipe_name,
                             profit=recipe_profit,
                             units=recipe_units if recipe_units > 0 else None)
            self.__insert__(recipe)
            if ingredients_:
                for ingredient_name, ingredient_amount in ingredients_:
                    self.add_ingredient2recipe(recipe_name=recipe_name,
                                               ingredient_name=ingredient_name,
                                               amount=ingredient_amount)
        return not recipe_exist

    @__capitalize__('ingredient_name', 'ingredient_unitype')
    def add_ingredient(self,
                       ingredient_name: str,
                       ingredient_cost: float,
                       ingredient_unitype: str,
                       ingredient_id: int = None
                       ) -> bool:

        ingredient_exist = self.query_get_ingredient(ingredient_name)
        if not ingredient_exist:
            ingredient = Ingredients(id=ingredient_id,
                                     name=ingredient_name,
                                     cost=ingredient_cost,
                                     unit_type=ingredient_unitype)
            self.__insert__(ingredient)
        return not ingredient_exist

    @__capitalize__('packaging_name')
    def add_packaging(self,
                      packaging_name: str,
                      packaging_cost: float,
                      packaging_profit: float,
                      packaging_id: int = None
                      ) -> bool:
        packaging_exist = self.query_get_packaging(packaging_name)
        if not packaging_exist:
            packaging = Packagings(id=packaging_id,
                                   name=packaging_name,
                                   cost=packaging_cost,
                                   profit=packaging_profit)
            self.__insert__(packaging)
        return not packaging_exist

    """Todas las funciones eliminar de Tabla Principal
    Estas funciones retornaran Type: bool"""

    def del_recipe(self,
                   recipe_name: str
                   ) -> bool:
        recipe_exist = self.query_get_recipe(recipe_name)
        if recipe_exist:
            recipe = recipe_exist
            self.session.delete(recipe)
            self.session.commit()
            return True
        return False

    def del_ingredient(self,
                       ingredient_name: str
                       ) -> bool:
        ingredient_exist = self.query_get_ingredient(ingredient_name)
        if ingredient_exist:
            ingredient = ingredient_exist
            self.session.delete(ingredient)
            self.session.commit()
            return True
        return False

    def del_packaging(self,
                      packaging_name: str
                      ) -> bool:
        packaging_exist = self.query_get_packaging(packaging_name)
        if packaging_exist:
            packaging = packaging_exist
            self.session.delete(packaging)
            self.session.commit()
            return True
        return False

    """Todas las funciones modificar precios de Tabla Principal
    Estas funciones retornaran Type: bool"""

    def mdf_profit_recipe(self,
                          recipe_name: str,
                          new_profit: float
                          ) -> bool:
        recipe_exist = self.query_get_recipe(recipe_name)
        if recipe_exist:
            recipe = recipe_exist
            recipe.profit = new_profit if new_profit > 0 else recipe.profit
            self.session.commit()
            return True
        return False

    def mdf_cost_ingredient(self,
                            ingredient_name: str,
                            new_cost: float
                            ) -> bool:
        ingredient_exist = self.query_get_ingredient(ingredient_name)
        if ingredient_exist:
            ingredient = ingredient_exist
            ingredient.cost = new_cost if new_cost > 0 else ingredient.cost
            self.session.commit()
            return True
        return False

    def mdf_cost_packaging(self,
                           packaging_name: str,
                           new_cost: float
                           ) -> bool:
        packaging_exist = self.query_get_packaging(packaging_name)
        if packaging_exist:
            packaging = packaging_exist
            packaging.cost = new_cost if new_cost > 0 else packaging.cost
            self.session.commit()
            return True
        return False

    """Todas las funciones añadir a Tabla Relacional
    Estas funciones retornaran Type: bool"""

    def add_ingredient2recipe(self,
                              recipe_name: str,
                              ingredient_name: str,
                              amount: float
                              ) -> bool:
        recipe_exist = self.query_get_recipe(recipe_name)
        ingredient_exist = self.query_get_ingredient(ingredient_name)
        try:
            recipe, ingredient = recipe_exist, ingredient_exist
            ingredient2recipe_exist = self.session.query(IngredientsRecipes).filter(
                (IngredientsRecipes.recipe_id == recipe.id) & (
                        IngredientsRecipes.ingredient_id == ingredient.id)).first()
        except AttributeError:
            return False
        except Exception as e:
            print(f"{type(e).__name__} error occurred: {e}")
            return False
        if not ingredient2recipe_exist:
            ingredient2recipe = IngredientsRecipes(recipe_id=recipe.id,
                                                   ingredient_id=ingredient.id,
                                                   amount=amount if amount > 0 else None)
            self.session.add(ingredient2recipe)
            self.session.commit()
        return not ingredient2recipe_exist

    def add_packaging2recipe(self,
                             recipe_name: str,
                             packaging_name: str,
                             amount: int
                             ) -> bool:
        recipe, packaging, packaging2recipe_exist = self.query_get_packaging2recipe(
            recipe_name, packaging_name, parent_to=True)
        if not packaging2recipe_exist:
            packaging2recipe = PackagingsRecipes(recipe_id=recipe.id,
                                                 packaging_id=packaging.id,
                                                 amount=amount if amount > 0 else None)
            self.session.add(packaging2recipe)
            self.session.commit()
        return not packaging2recipe_exist


"""Creacion y relacion con toda la DB"""
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
DBM = _DBManager(session)


def main():
    """Testing del la DB"""
    print(DBM.add_ingredient("azucar", 500, "kg", ingredient_id=100))
    print(DBM.add_ingredient("harina 0000", 600, "kg"))
    print(DBM.add_ingredient("harina 000", 1230, "kg"))
    print(DBM.add_ingredient("leche", 400, 'litro'))
    print(DBM.add_recipe("torta", 3.0, 1, [('azucar', .5), ('harina 000', .7),
                                         ('aceituna', 1), ('harina 0000', 2)]))
    print(DBM.add_recipe("alfajores", 3, 12, [('harina 000', .8), ('leche', 1)]))
    print(DBM.add_packaging("caja x8 marplatense", 69, 1.5))
    print(DBM.add_ingredient2recipe('torta', 'leche', 0.5))
    print(DBM.add_packaging2recipe('torta', 'caja x8 marplatense', 1))
    print(DBM.add_packaging2recipe('alfajores', 'caja x8 marplatense', 6))


if __name__ == "__main__":
    main()
