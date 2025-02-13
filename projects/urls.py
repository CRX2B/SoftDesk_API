from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('issues', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')
router.register('contributors', ContributorViewSet, basename='contributor')

urlpatterns = router.urls
