from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 15:
        raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
    
    
class User(AbstractUser):
    birth_date = models.DateField(validators=[validate_age])
    consent = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    last_password_update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def delete_personnal_data(self):
        self.username = "Utilisateur supprimé"
        self.email = None
        self.birth_date = None
        self.consent = False
        self.can_be_contacted = False
        self.can_data_be_shared = False
        self.is_active = False
        self.save()

    def clean(self):
        if not self.is_superuser and not self.birth_date:
            raise ValidationError("La date de naissance est obligatoire.")
        super().clean()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.consent = True
            if not self.birth_date:
                self.birth_date = date(1900, 1, 1)
        self.clean()
        super().save(*args, **kwargs)
