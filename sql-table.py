from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import orm

engine = create_engine('sqlite:///ph_database.db')

Base = orm.declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class RecipeIngredients(Base):
    """Crear una tabla que contenga la union de las dos tablas"""
    __tablename__: str = 'ingredients2recipes'
    
    id = Column(Integer, primary_key= True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable= False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable= False)
    ammunt = Column(Float, nullable= False, default= 1.00)
    
    "Relacion unidireccional de RecipeIngredients > Ingredients"
    ingredient= relationship("Ingredients")

class Recipes(Base):
    """Creacion de la tabla de Recetas, esta tiene una relacion con la tabla recipe_rawm_association,
    de esta forma se relaciona de forma directa con todos los ingredientes requeridos"""
    __tablename__: str = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    "Relacion unidireccional de Recipes > RecipeIngredients"
    ingredients = relationship("RecipeIngredients", cascade="delete")

class Ingredients(Base):
    """Creacion de la tabla de Materia Prima"""
    __tablename__: str = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit_type = Column(String, nullable=False, default="kg") # Existen (unidad, kg, litro)
    

class DBManager:
    def __int__(self, session):
        self.session: orm.session.Session = session

    def add_recipe(self, recipe_name: str, its_ingredients: list):
        """Creamos una receta nueva este debe entregar una lista de ingredientes tipo tupla, uno su nombre y en la otra su cantidad"""
        recipe = self.session.query(Recipes).filter_by(name= recipe_name).first()
        if not recipe: #Entra si no existe recipe
            new_recipe = Recipes(name=recipe_name.capitalize())
            for ingredient_name, amount in its_ingredients:
                ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
                ingredient2recipe = RecipeIngredients(recipe_id=new_recipe.id, ingredient_id=ingredient.id, amount=amount)
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
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id, ingredient_id=ingredient.id).first()
        
        if not ingredient2recipe: #Entra si no existe ingredient2recipe
            ingredient2recipe = RecipeIngredients(recipe_id=recipe.id, ingredient_id=ingredient.id, amount=amount)
            self.session.add(ingredient2recipe)
            self.session.commit()
            
    def modify_rw2recipe(self, recipe_name: str, ingredient_name: str, amount: float):
        """Modifica la cantidad necesaria de un ingrediente en la receta"""
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id, ingredient_id=ingredient.id).first()
        
        if ingredient2recipe: #Entra si existe ingrediente2recipe
            ingredient2recipe.amount= amount
            self.session.commit()
    
    def remove_rw2recipe(self, recipe_name: str, ingredient_name: str):
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        ingredient2recipe = self.session.query(RecipeIngredients).filter_by(recipe_id=recipe.id, ingredient_id=ingredient.id).first()
        
        self.session.delete(ingredient2recipe)
        self.session.commit()
            
    def print_rw2recipe(self, recipe_name: str):
        recipe = self.session.query(Recipes).filter_by(name=recipe_name.capitalize()).first()
        print(f"Receta: {recipe.name}\n")
        
        if recipe: #Entra si existe recipe
            for rw in recipe.ingredients:
                print(f"{rw.ingredient.name} $ {rw.ingredient.price}")
                
    def add_ingredient(self, ingredient_name: str, ingredient_price: int, ingredient_unitype: str= None):
        ingredient = Ingredients(name=ingredient_name.capitalize(), price=ingredient_price)
        
        if ingredient_unitype:
            ingredient.unit_type = ingredient_unitype
        
        self.session.add(ingredient)
        self.session.commit()
        
    def modify_price(self, ingredient_name: str, new_price: float):
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        
        if new_price > 0:
            ingredient.price = new_price
        
        self.session.commit()
        
    def delete_ingredient(self, ingredient_name: str):
        ingredient = self.session.query(Ingredients).filter_by(name=ingredient_name.capitalize()).first()
        
        self.session.delete(ingredient)
        self.session.commit()
        
        