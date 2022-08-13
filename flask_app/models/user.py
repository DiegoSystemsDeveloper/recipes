from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)

        if not len(result) > 0:
            return False
        else:
            return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result = connectToMySQL('recetas_schema').query_db(query, data)
        return cls(result[0])

    @staticmethod
    def user_validate_sign_up(data):
        es_valido = True
        if len(data['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        if len(data['last_name']) < 3:
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        if not EMAIL_REGEX.match(data['email']):
            flash('Email invalido', 'registro')
            es_valido = False

        if len(data['password']) < 6:
            flash('Password debe tener almenos 6 caracteres', 'registro')
            es_valido = False

        number = False
        upper = False
        for character in data['password']:
            if character.isupper():
                upper = True
            if character.isnumeric():
                number = True

        if not number:
            flash('El password debe contener almenos un numero', 'registro')
            es_valido = False
        if not upper:
            flash('El password debe contener almenos una letra en mayuscula', 'registro')
            es_valido = False

        if data['password'] != data['conf_password']:
            flash('Password no coinciden', 'registro')
            es_valido = False

        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas_schema').query_db(query, data)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False

        return es_valido

    @staticmethod
    def user_validate_sign_in(data):
        if not len(data['email']) > 0:
            flash('Por favor llene los campos', 'login')
            return False

        if not EMAIL_REGEX.match(data['email']):
            flash('Email invalido', 'login')
            return False

        if not len(data['password']) > 0:
            flash('Por favor llene los campos', 'login')
            return False
        return True

        

    

        



