from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request):
        """
        Endpoint pour gérer son propre compte utilisateur.
        GET: récupère ses informations
        PUT/PATCH: met à jour ses informations
        DELETE: supprime son compte (anonymisation)
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
            
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
        elif request.method == 'DELETE':
            user.delete_personnal_data()  # Méthode déjà existante dans le modèle User
            return Response(status=204)
