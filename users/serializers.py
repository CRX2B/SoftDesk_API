from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User.
    
    Permet de sérialiser et désérialiser les données des utilisateurs,
    de créer un utilisateur avec un mot de passe sécurisé et de valider la cohérence
    des champs liés au consentement (RGPD).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birth_date', 'consent', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        """
        Crée un utilisateur avec un mot de passe sécurisé.
        
        :param validated_data: Les données validées pour la création.
        :return: L'instance de User créée.
        """
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        """
        Valide la cohérence des champs liés au consentement.
        
        Si l'utilisateur souhaite être contacté ou partager ses données, il doit avoir donné son consentement global.
        
        :param data: Données soumises.
        :raises serializers.ValidationError: Si le consentement n'est pas présent quand requis.
        :return: Les données validées.
        """
        if data.get('can_be_contacted') or data.get('can_data_be_shared'):
            if not data.get('consent', False):
                raise serializers.ValidationError("Le consentement global est requis pour les autres options RGPD.")
        return data