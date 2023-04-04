from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from custom_types.views import CustomTypeViewSet
from ledgers.views import LedgerViewSet, SharedLedgerViewSet
from monthly_budgets.views import MonthlyBudgetViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("monthly-budgets", MonthlyBudgetViewSet, basename="monthly-budgets")
router.register("custom-types", CustomTypeViewSet, basename="custom-types")
router.register("ledgers", LedgerViewSet, basename="ledgers")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "<str:token>",
        SharedLedgerViewSet.as_view({"get": "retrieve"}),
        name="shared-ledger",
    ),
    path(
        "api/ledgers/<int:pk>/share",
        LedgerViewSet.as_view(
            {"post": "share_ledger", "delete": "delete_shared_ledger"}
        ),
        name="ledgers-share",
    ),
]

# swagger
urlpatterns += [
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# Simple JWT
urlpatterns += [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
