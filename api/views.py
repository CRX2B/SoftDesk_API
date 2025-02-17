from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)
from .permissions import IsAuthorOrReadOnly, IsProjectAuthor
from .mixins import ContributorPermissionMixin, ProjectContextMixin, IssueContextMixin


class ProjectViewSet(ModelViewSet):
    """
    ViewSet pour gérer les projets.

    Permet aux utilisateurs de visualiser la liste des projets auxquels ils contribuent.
    L'auteur du projet peut créer, modifier ou supprimer son propre projet.
    Lors de la création, l'utilisateur est automatiquement ajouté comme contributeur.
    """

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        """
        Retourne la liste des projets auxquels l'utilisateur authentifié contribue.
        """
        return (
            Project.objects.filter(contributors=self.request.user)
            .order_by("created_time")
            .prefetch_related("contributors")
        )

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
        Retourne la liste des tickets appartenant au projet spécifié dans l'URL,
        en s'assurant que l'utilisateur authentifié est contributeur du projet.
        """
        project = (
            self.get_project()
        )  # Utilisation du mixin pour récupérer l'objet projet
        return (
            Issue.objects.filter(
                project=project, project__contributors=self.request.user
            )
            .order_by("created_time")
            .select_related("project", "author", "assignee")
        )

    def perform_create(self, serializer):
        """
        Crée un ticket pour un projet auquel l'utilisateur contribue.
        """
        project = self.get_project()
        self.check_project_permission(project)
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(IssueContextMixin, ContributorPermissionMixin, ModelViewSet):
    """
    ViewSet pour gérer les commentaires associés aux tickets (issues).

    Seuls les contributeurs du projet peuvent ajouter ou consulter les commentaires.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne la liste des commentaires pour l'issue renseignée dans l'URL.
        """
        issue = self.get_issue()  # Utilisation du mixin pour récupérer l'objet issue
        return (
            Comment.objects.filter(
                issue=issue, issue__project__contributors=self.request.user
            )
            .order_by("created_time")
            .select_related("issue", "author")
        )

    def perform_create(self, serializer):
        """
        Crée un commentaire pour une issue.
        """
        issue = self.get_issue()
        self.check_project_permission(issue.project)
        serializer.save(author=self.request.user, issue=issue)


class ContributorViewSet(ProjectContextMixin, ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d'un projet.

    Seul l'auteur du projet peut ajouter, modifier ou retirer des contributeurs.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        project = self.get_project()  # Récupération de l'instance projet grâce au mixin
        return (
            Contributor.objects.filter(project=project)
            .order_by("created_time")
            .select_related("project", "user")
        )

    def perform_create(self, serializer):
        project = (
            self.get_project()
        )  # Utilisation du mixin pour récupérer l'objet projet
        if project.author != self.request.user:
            raise PermissionDenied(
                "Seul l'auteur du projet peut ajouter des contributeurs."
            )
        serializer.save(project=project)
