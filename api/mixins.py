from rest_framework.exceptions import PermissionDenied
from .models import Contributor, Project, Issue
from django.shortcuts import get_object_or_404

class ContributorPermissionMixin:
    def check_project_permission(self, project):
        """
        Vérifie que l'utilisateur authentifié est contributeur du projet passé en paramètre.
        """
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")

class ProjectContextMixin:
    def get_project(self):
        project_pk = self.kwargs.get('project_pk')
        return get_object_or_404(Project, pk=project_pk)

class IssueContextMixin:
    def get_issue(self):
        issue_pk = self.kwargs.get('issue_pk')
        return get_object_or_404(Issue, pk=issue_pk) 