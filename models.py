import psycopg2
import os
from werkzeug.security import generate_password_hash

class PythonSQL:
    def __init__(self):
        # Connexion à la base PostgreSQL via l'URL dans la variable d'environnement DATABASE_URL
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def selectData(self, req, params=None):
        try:
            if params:
                self.cursor.execute(req, params)
            else:
                self.cursor.execute(req)
            return self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()  # 🔴 ANNULATION de la transaction en cas d'erreur
            print("Erreur SQL:", e)  # affichage de l'erreur
            return None

    def insertData(self, table, email, password):
        hashed_password = generate_password_hash(password)
        req = f"INSERT INTO {table} (email, password) VALUES (%s, %s)"
        self.cursor.execute(req, (email, hashed_password))
        self.conn.commit()

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.email}')"
