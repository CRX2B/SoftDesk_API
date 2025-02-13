from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(ModelViewSet):
    """
    Vue pour gérer les utilisateurs (CRUD)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        -Permet à tout le monde de créer un compte (POST).
        -Exige une authentification JWT pour toutes les autres actions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Limite la visibilité des données utilisateurs à l'utilisateur connecté uniquement.
        """
        return self.queryset.filter(id=self.request.user.id)