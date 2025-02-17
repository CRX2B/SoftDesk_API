from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(ModelViewSet):
    """
    Vue pour gérer les opérations CRUD sur les utilisateurs.

    - La création d'un compte (POST) est accessible à tous.
    - Les opérations de lecture, mise à jour et suppression nécessitent une authentification JWT.
    - Chaque utilisateur ne peut accéder qu'à ses propres données.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Détermine les permissions en fonction de l'action :
          - Permet à tout le monde de créer un compte.
          - Exige une authentification pour toutes les autres actions.

        :return: Liste d'instances de permission.
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Restreint le queryset à l'utilisateur authentifié afin que chacun
        ne puisse accéder qu'à ses propres données.

        :return: Queryset filtré par l'ID de l'utilisateur connecté.
        """
        return self.queryset.filter(id=self.request.user.id)
