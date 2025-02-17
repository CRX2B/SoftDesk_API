from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, ProjectListSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectAuthor
from rest_framework.decorators import action
from rest_framework.response import Response
from .mixins import ContributorPermissionMixin, ProjectContextMixin


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
        return Project.objects.filter(contributors=self.request.user).order_by('created_time').prefetch_related('contributors')
    
    def perform_create(self, serializer):
        """
        Crée un projet et ajoute automatiquement l'auteur comme contributeur.
        
        :param serializer: Le serializer validé pour la création d'un projet.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class IssueViewSet(ProjectContextMixin, ContributorPermissionMixin, ModelViewSet):
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
        Si 'project_pk' est présent dans l'URL, on restreint le queryset aux tickets du projet spécifié.
        """
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            return Issue.objects.filter(
                project__id=project_pk,
                project__contributors=self.request.user
            ).order_by('created_time').select_related('project', 'author', 'assignee')
        return Issue.objects.filter(
            project__contributors=self.request.user
        ).order_by('created_time').select_related('project', 'author', 'assignee')
    
    def perform_create(self, serializer):
        """
        Crée un ticket pour un projet auquel l'utilisateur contribue.
        Si 'project_pk' est présent dans l'URL, le ticket est automatiquement lié à ce projet.
        """
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            project = Project.objects.get(pk=project_pk)
            self.check_project_permission(project)
            serializer.save(author=self.request.user, project=project)
        else:
            project = serializer.validated_data['project']
            self.check_project_permission(project)
            serializer.save(author=self.request.user)
        
        
class CommentViewSet(ContributorPermissionMixin, ModelViewSet):
    """
    ViewSet pour gérer les commentaires associés aux tickets (issues).
    
    Seuls les contributeurs du projet peuvent ajouter ou consulter les commentaires.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        """
        Retourne la liste des commentaires pour les tickets des projets auxquels l'utilisateur contribue.
        Si 'issue_pk' est présent dans l'URL, on restreint le queryset aux commentaires de l'issue spécifiée.
        """
        issue_pk = self.kwargs.get('issue_pk')
        if issue_pk:
            return Comment.objects.filter(
                issue__id=issue_pk,
                issue__project__contributors=self.request.user
            ).order_by('created_time').select_related('issue', 'author')
        return Comment.objects.filter(
            issue__project__contributors=self.request.user
        ).order_by('created_time').select_related('issue', 'author')
    
    def perform_create(self, serializer):
        """
        Crée un commentaire pour une issue.
        Si 'issue_pk' est présent dans l'URL, le commentaire est automatiquement lié à cette issue.
        """
        issue_pk = self.kwargs.get('issue_pk')
        if issue_pk:
            issue = Issue.objects.get(pk=issue_pk)
            self.check_project_permission(issue.project)
            serializer.save(author=self.request.user, issue=issue)
        else:
            issue = serializer.validated_data['issue']
            self.check_project_permission(issue.project)
            serializer.save(author=self.request.user)
        
        
class ContributorViewSet(ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d'un projet.
    
    Seul l'auteur du projet peut ajouter, modifier ou retirer des contributeurs.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    
    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        return Contributor.objects.filter(project__id=project_pk).order_by('created_time').select_related('project', 'user')
    
    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_pk)
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")
        serializer.save(project=project)