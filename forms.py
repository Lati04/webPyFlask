from models import PythonSQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, ValidationError
import re

# Messages d'erreur personnalisés
custom_error_messages = {
    'email required': 'L\'Email est requis.',
    'email_invalid_format': 'Format d\'email invalide.',
    'email_length': 'L\'email doit avoir une longueur comprise entre 6 et 35 caractères.',
    'email_already_exists': 'Cet email est déjà connu.',
    'password_required': 'Mot de passe requis',
    'password_length': 'Le mot de passe doit contenir au moins 8 caractères.',
    'password_complexity': 'Le mot de passe doit contenir au moins un chiffre, une minuscule et une majuscule.'
}

class SignupForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Mot de Passe', [
        validators.EqualTo('confirm', message='les mots de passe doivent correspondre.')
    ])
    confirm = PasswordField('Confirmer le mot de passe.')
    submit = SubmitField('Valider')

    def validate_email(self, email):
        if not email.data:
            raise ValidationError(custom_error_messages['email required'])
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError(custom_error_messages['email_invalid_format'])
        
        if len(email.data) < 6 or len(email.data) > 35:
            raise ValidationError(custom_error_messages['email_length'])
        
        # ✅ On crée la connexion ici, pas au chargement du fichier
        connexion_sql = PythonSQL()
        req = "SELECT * FROM users WHERE email = %s"
        results = connexion_sql.selectData(req, (email.data,))
        if results:
            raise ValidationError(custom_error_messages['email_already_exists'])

    def validate_password(self, password):
        if not password.data:
            raise ValidationError(custom_error_messages['password_required'])
        
        if len(password.data) < 8:
            raise ValidationError(custom_error_messages['password_length'])
        
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', password.data):
            raise ValidationError(custom_error_messages['password_complexity'])

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Mot de Passe')
    submit = SubmitField('Valider')

    def validate_email(self, email):
        if not email.data:
            raise ValidationError(custom_error_messages['email required'])
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError(custom_error_messages['email_invalid_format'])
        
        if len(email.data) < 6 or len(email.data) > 35:
            raise ValidationError(custom_error_messages['email_length'])

    def validate_password(self, password):
        if not password.data:
            raise ValidationError(custom_error_messages['password_required'])
