from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls + [
    path("register/", UserViewSet.as_view({"post": "create"}), name="user-register"),
    path("login/", TokenObtainPairView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
