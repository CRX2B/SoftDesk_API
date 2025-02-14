from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validate_age(birth_date):
    """
    Valide que l'utilisateur a au moins 15 ans pour s'inscrire.
    
    :param birth_date: Date de naissance de l'utilisateur.
    :raises ValidationError: Si l'utilisateur a moins de 15 ans.
    """
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 15:
        raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
    
    
class User(AbstractUser):
    """
    Modèle utilisateur étendu basé sur AbstractUser.
    
    Champs additionnels :
      - birth_date : Date de naissance (vérifiée pour s'assurer que l'utilisateur a au moins 15 ans).
      - consent : Indique si l'utilisateur a consenti au traitement de ses données (RGPD).
      - can_be_contacted : Autorise à contacter l'utilisateur.
      - can_data_be_shared : Autorise le partage des données de l'utilisateur.
    
    Méthodes spéciales :
      - delete_personnal_data : Anonymise et supprime les données personnelles.
      - clean : Effectue des validations supplémentaires, notamment que la date de naissance soit renseignée.
      - save : Applique des règles spécifiques (notamment pour les superutilisateurs) avant de sauvegarder.
    """
    birth_date = models.DateField(validators=[validate_age])
    consent = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    last_password_update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de l'utilisateur (son username).
        """
        return self.username
    
    def delete_personnal_data(self):
        """
        Anonymise et supprime les données personnelles de l'utilisateur pour se conformer au droit à l'oubli.
        """
        self.username = "Utilisateur supprimé"
        self.email = None
        self.birth_date = None
        self.consent = False
        self.can_be_contacted = False
        self.can_data_be_shared = False
        self.is_active = False
        self.save()

    def clean(self):
        """
        Effectue des validations supplémentaires avant la sauvegarde.
        Vérifie que la date de naissance est renseignée pour les utilisateurs non superutilisateurs.
        """
        if not self.is_superuser and not self.birth_date:
            raise ValidationError("La date de naissance est obligatoire.")
        super().clean()

    def save(self, *args, **kwargs):
        """
        Sauvegarde l'utilisateur en appliquant des règles spécifiques.
        
        Pour les superutilisateurs :
          - Le consentement est automatiquement activé.
          - Si la date de naissance est manquante, une valeur par défaut (1900-01-01) est assignée.
        
        La méthode clean() est ensuite appelée pour valider les données avant la sauvegarde.
        """
        if self.is_superuser:
            self.consent = True
            if not self.birth_date:
                self.birth_date = date(1900, 1, 1)
        self.clean()
        super().save(*args, **kwargs)
