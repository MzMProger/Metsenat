from rest_framework.viewsets import ModelViewSet
from apps.sponsors.models import Sponsor
from apps.sponsors.permissions import SponsorPermission
from apps.sponsors.serializers import (
    SponsorSerializer,
    SponsorCreateSerializer,
    SponsorUpdateSerializer,
    SponsorListSerializer,
    SponsorDetailSerializer
)
# from rest_framework.permissions import IsAuthenticated, AllowAny


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [SponsorPermission]

    # def get_permissions(self):
    #     if self.action == "create":
    #         return [AllowAny]
    #     return [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return SponsorCreateSerializer
        elif self.action in ("update", "partial_update"):
            return SponsorUpdateSerializer
        elif self.action == "list":
            return SponsorListSerializer
        elif self.action == "retrieve":
            return SponsorDetailSerializer
        return self.serializer_class
