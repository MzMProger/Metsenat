from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.core.views import DashboardViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("dashboards", DashboardViewSet, basename="dashboards")

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls