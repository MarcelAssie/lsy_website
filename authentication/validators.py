import re
from django.core.exceptions import ValidationError

class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Le mot de passe doit contenir au moins une majuscule.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Le mot de passe doit contenir au moins une minuscule.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Le mot de passe doit contenir au moins un chiffre.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Le mot de passe doit contenir au moins un caractère spécial.')
    def get_help_text(self):
        return (
            "Votre mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre et un caractère spécial."
        )

class MaxLengthValidator:
    def __init__(self, max_length=12):
        self.max_length = max_length
    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(f"Le mot de passe ne peut pas dépasser {self.max_length} caractères.")
    def get_help_text(self):
        return f"Votre mot de passe ne peut pas dépasser {self.max_length} caractères."

    


