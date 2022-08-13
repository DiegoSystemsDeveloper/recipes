from cgitb import reset
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s, %(user_id)s)'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = 'SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id'
        results = connectToMySQL('recetas_schema').query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under30 = %(under30)s WHERE id = %(id)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return result

    @classmethod
    def delete_recipe(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return result

    @staticmethod
    def valida_receta(data):
        es_valido = True

        if len(data['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'recetas')
            es_valido = False

        if len(data['description']) < 3:
            flash('La descripcion de la receta debe tener al menos 3 caracteres', 'recetas')
            es_valido = False

        if len(data['instructions']) < 3:
            flash('Las instrucciones de la receta debe tener al menos 3 caracteres', 'recetas')
            es_valido = False

        if not len(data['date_made']) > 3:
            flash('Ingrese una fecha', 'recetas')
            es_valido = False

        return es_valido

    @staticmethod
    def validate_join_recipe(data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s and user_id = %(user_id)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        if not len(result) > 0:
            return False
        return True
