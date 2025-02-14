from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Permission personnalisée permettant uniquement à l'auteur
    de modifier ou supprimer la ressource.
    Les autres utilisateurs (et notamment les contributeurs) ne peuvent que consulter.
    """
    def has_object_permission(self, request, view, obj):
        # Autoriser la lecture pour toute méthode sûre (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Pour les autres méthodes, vérifier que l'utilisateur est bien l'auteur
        return hasattr(obj, 'author') and obj.author == request.user

class IsProjectAuthor(BasePermission):
    """
    Permission personnalisée pour la gestion des contributeurs.
    Seul l'auteur du projet peut ajouter, modifier ou supprimer des contributeurs.
    """
    def has_object_permission(self, request, view, obj):
        # Ici, obj est une instance de Contributor ; on vérifie que l'auteur du projet est l'utilisateur courant
        return obj.project.author == request.user 