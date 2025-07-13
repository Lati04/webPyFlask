from mysql import connector
from werkzeug.security import generate_password_hash

class PythonSQL:
      def __init__(self):
            self.db = connector.connect(
                  user='root',
                  password='',
                  database='FlaskSqlDevoir',
                  host='localhost'
            ) 
            self.ma_bdd = self.db.cursor()

      def __del__(self):
            self.db.close()

      def selectData(self, req, params=None):
            if params: 
                self.ma_bdd.execute(req, params)
            else:
                 self.ma_bdd.execute(req)
            return self.ma_bdd.fetchall()
      
      def insertData(self, table, email, password):
            hashed_password = generate_password_hash(password)
            req = "INSERT INTO users (email, password) VALUES (%s, %s)"
            values = (email, hashed_password)

            self.ma_bdd.execute(req, values)
            self.db.commit()  
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.email}')"