from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birth_date', 'consent', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        """
        Crée un utilisateur avec un mot de passe sécurisé.
        """
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        """
        Valide que les champs liés au consentement sont cohérents.
        """
        if data.get('can_be_contacted') or data.get('can_data_be_shared'):
            if not data.get('consent', False):
                raise serializers.ValidationError("Le consentement global est requis pour les autres options RGPD.")
        return data