from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission personnalisée permettant uniquement à l'auteur
    de modifier ou supprimer la ressource.
    Les autres utilisateurs (et notamment les contributeurs) ne peuvent que consulter.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(obj, "author") and obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Permission personnalisée pour la gestion des contributeurs.
    Seul l'auteur du projet peut ajouter, modifier ou supprimer des contributeurs.
    """

    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user
