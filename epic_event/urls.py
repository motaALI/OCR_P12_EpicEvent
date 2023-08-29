from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from contractManager.api.views import (
    ClientViewSet,
    ContractViewSet,
    UserViewSet,
    EventViewSet,
    RoleViewSet,
    ObtainTokenPairView,
    RegisterViewSet,
)

outer_router = routers.SimpleRouter()

outer_router.register(r"roles", RoleViewSet, basename="roles")
outer_router.register(r"users", UserViewSet, basename="users")
outer_router.register(r"clients", ClientViewSet, basename="clients")
outer_router.register(r"contracts", ContractViewSet, basename="contracts")
outer_router.register(r"events", EventViewSet, basename="events")

client_router = routers.NestedSimpleRouter(outer_router, r"clients", lookup="client")
contract_router = routers.NestedSimpleRouter(
    outer_router, r"contracts", lookup="contract"
)

client_router.register(r"events", EventViewSet, basename="client-events")
contract_router.register(r"events", EventViewSet, basename="contract-events")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("login/", ObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterViewSet.as_view(), name="auth_register"),
    path("api/", include(outer_router.urls)),
    path("api/", include(client_router.urls)),
    path("api/", include(contract_router.urls)),
]
