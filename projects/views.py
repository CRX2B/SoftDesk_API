from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, ProjectListSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectAuthor


class ProjectViewSet(ModelViewSet):
    """
    ViewSet pour gérer les projets.
    
    Permet aux utilisateurs de visualiser la liste des projets auxquels ils contribuent.
    L'auteur du projet peut créer, modifier ou supprimer son propre projet.
    Lors de la création, l'utilisateur est automatiquement ajouté comme contributeur.
    """
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        """
        Retourne la liste des projets auxquels l'utilisateur authentifié contribue.
        """
        return Project.objects.filter(contributors=self.request.user).prefetch_related('contributors')
    
    def perform_create(self, serializer):
        """
        Crée un projet et ajoute automatiquement l'auteur comme contributeur.
        
        :param serializer: Le serializer validé pour la création d'un projet.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
    

class IssueViewSet(ModelViewSet):
    """
    ViewSet pour gérer les tickets (issues) liés aux projets.
    
    Seuls les contributeurs du projet peuvent accéder aux tickets.
    Lors de la création, l'utilisateur est assigné comme auteur du ticket.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        """
        Retourne la liste des tickets appartenant aux projets dans lesquels l'utilisateur contribue.
        """
        return Issue.objects.filter(project__contributors=self.request.user).select_related('project', 'author', 'assignee')
    
    def perform_create(self, serializer):
        """
        Crée un ticket pour un projet auquel l'utilisateur contribue.
        Vérifie que l'utilisateur est bien contributeur du projet.
        
        :param serializer: Le serializer validé pour la création d'une issue.
        """
        project = serializer.validated_data['project']
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
        serializer.save(author=self.request.user)
        
        
class CommentViewSet(ModelViewSet):
    """
    ViewSet pour gérer les commentaires associés aux tickets (issues).
    
    Seuls les contributeurs du projet peuvent ajouter ou consulter les commentaires.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        """
        Retourne la liste des commentaires pour les tickets des projets auxquels l'utilisateur contribue.
        """
        return Comment.objects.filter(issue__project__contributors=self.request.user).select_related('issue', 'author')
    
    def perform_create(self, serializer):
        """
        Crée un commentaire pour une issue.
        Vérifie que l'utilisateur est contributeur du projet associé à l'issue.
        
        :param serializer: Le serializer validé pour la création d'un commentaire.
        """
        issue = serializer.validated_data['issue']
        if not Contributor.objects.filter(user=self.request.user, project=issue.project).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
        serializer.save(author=self.request.user)
        
        
class ContributorViewSet(ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d'un projet.
    
    Seul l'auteur du projet peut ajouter, modifier ou retirer des contributeurs.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    
    def get_queryset(self):
        """
        Retourne la liste des contributeurs pour les projets dont l'utilisateur est l'auteur.
        """
        return Contributor.objects.filter(project__author=self.request.user).select_related('project', 'user')
    
    def perform_create(self, serializer):
        """
        Ajoute un nouveau contributeur à un projet.
        Vérifie que l'utilisateur effectuant l'ajout est bien l'auteur du projet.
        
        :param serializer: Le serializer validé pour la création d'un contributeur.
        """
        project = serializer.validated_data['project']
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")
        serializer.save()