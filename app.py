from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash

from config import Config
from forms import SignupForm
from forms import LoginForm
from models import PythonSQL, User

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

user_connected = []

def isUserCo():
	if len(user_connected) != 0:
		return True
	else:
		return False

# Route pour la page d'accueul
@app.route('/', methods=['GET'])
def routePrincipal():
      if len(user_connected) != 0:
            contenu = 'Bonjour ' + user_connected[0] 
      else:
            contenu = "Bonjour utilisateur anonyme"

      return render_template(
            'home.html',
            title= 'Home',
            data= contenu,
            menu_user_co=isUserCo())  

# Route pour la page de signup
@app.route('/signup', methods=['GET', 'POST'])
def routeSignup():
      form = SignupForm()

      if request.method == 'POST' and form.validate_on_submit():
       
            user = User(form.email.data, form.password.data)
           
            inscription_sql=PythonSQL()
            inscription_sql.insertData('users', user.email, user.password)
            flash('Merci d\'avoir crée votre compte, vous pouvez vous logger', 'success')
            return render_template(
			'signup.html',
			 title="Signup",
                   form=form,
			 user_inscrit = True,
			menu_user_co=isUserCo()
			)
      else:
            return render_template(
                        'signup.html',
                        title="Signup",
                        form=form,
                        menu_user_co=isUserCo()
                  ) 

# Route pour la page de login
@app.route('/login', methods=['GET', 'POST'])
def routeLogin():
      form = LoginForm()
      print(LoginForm())

      if request.method == 'POST' and form.validate_on_submit():
  
            user = User(form.email.data, form.password.data)
            
            #Vérifier si l'utilisateur existe dans la base de données
            connexion_sql = PythonSQL()
        
            user_data = connexion_sql.selectData("SELECT * FROM users WHERE email = %s", (user.email,))

            if user_data and check_password_hash(user_data[0][2], user.password):
      
                  user_connected.append(user.email)
                  flash('Vous êtes connecté(e)', 'success')
                  # Ajouter l'utilisateur à la liste des utilisateurs connectés
                  return redirect(url_for('routePrincipal'))
            
            else:
                  flash('Utilisateur non connu', 'danger')
                  return render_template(
                        'login.html',
                        title='Login',
                        form=form,
                        menu_user_co=isUserCo())
      else:    
            return render_template(
                  'login.html',
                  title='Login',
                  form=form,
                  menu_user_co=isUserCo()
            )    
      
# Route pour la deconnexion
@app.route('/logout', methods=['GET'])
def routeLogout():
      user_connected.clear()
      return redirect(url_for('routePrincipal'))
    
@app.errorhandler(404)
def error404(code):
	return render_template(
		'pagenotfound.html',
		title='Page 404',
		menu_user_co=isUserCo()
	)

if __name__=='__main__':
    app.run(debug=True)