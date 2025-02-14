from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly, IsProjectAuthor


class ProjectViewSet(ModelViewSet):
    """
    ViewSet pour gérer les projets.
    Seuls les contributeurs peuvent voir un projet.
    Seul l'auteur peut modifier ou supprimer un projet.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
    

class IssueViewSet(ModelViewSet):
    """
    ViewSet pour gérer les tickets liés au projets.
    Seuls les contributeurs du projet peuvent voir et créer des issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Issue.objects.filter(project__contributors=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
        serializer.save(author=self.request.user)
        
        
class CommentViewSet(ModelViewSet):
    """
    ViewSet pour gérer les commentaires liés aux issues.
    Seuls les contributeurs du projet peuvent voir et créer des commentaires.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributors=self.request.user)
    
    def perform_create(self, serializer):
        issue = serializer.validated_data['issue']
        if not Contributor.objects.filter(user=self.request.user, project=issue.project).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
        serializer.save(author=self.request.user)
        
        
class ContributorViewSet(ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d'un projet.
    Seul l'auteur du projet peut ajouter ou retirer des contributeurs.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    
    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")
        serializer.save()