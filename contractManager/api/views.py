from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from contractManager.api.permissions import (IsManagementUser, IsSalesUser,
                                             IsSupportUser)
from contractManager.api.serializers import (ClientSerializer,
                                             ContractSerializer,
                                             CustomUserSerializer,
                                             EventSerializer,
                                             RegisterSerializer,
                                             RoleSerializer,
                                             TokenObtainPairSerializer)
from contractManager.models import Client, Contract, CustomUser, Event, Role


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


class RegisterViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get_permissions(self):

        method_classes = {
            "list": [IsAuthenticated],
            "create": [IsSupportUser],
            "retrieve": [IsAuthenticated],
            "update": [IsAuthenticated, IsSupportUser],
            "partial_update": [IsAuthenticated, IsSupportUser],
            "destroy": [IsAuthenticated, IsSupportUser],
        }

        if self.action in method_classes:
            print(
                f"Connected User Role before permission check: {self.request.user.role}"
            )
            return [permission() for permission in method_classes[self.action]]
        else:
            return super().get_permissions()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsManagementUser]
    filter_backends = [SearchFilter]
    search_fields = ["full_name", "phone", "company_name", "sales_contact"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            if self.request.user.role == Role.SALES:
                return [IsAuthenticated(), IsSalesUser()]
            else:
                return [IsAdminUser()]  # Assuming admin can perform these actions
        elif self.action == "list":
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    @action(detail=True, methods=["GET"])
    def contracts(self, request, pk=None):
        client = self.get_object()
        contracts = Contract.objects.filter(client=client)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def create_event(self, request, pk=None):
        client = self.get_object()
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # Set the client and save the event
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["client", "sales_contact"]

    def get_permissions(self):
        if self.request.user.role == Role.SALES:
            return [IsAuthenticated(), IsSalesUser()]
        elif self.request.user.role == Role.SUPPORT:
            return [IsAuthenticated(), IsSupportUser()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == Role.SALES:
            queryset = queryset.filter(client__sales_contact=self.request.user)
        return queryset

    @action(detail=True, methods=["POST"])
    def create_contract(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsManagementUser]
    filter_backends = [SearchFilter]
    search_fields = ["contract", "client_name", "client_contact"]

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            if self.request.user.role == Role.SUPPORT:
                return [IsAuthenticated(), IsSupportUser()]
            else:
                return [IsAdminUser()]  # Assuming admin can perform these actions
        elif self.action == "list":
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        if self.request.user.role == Role.SUPPORT:
            return Event.objects.filter(support_associated=self.request.user)
        else:
            return Event.objects.all()
