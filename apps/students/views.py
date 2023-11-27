from rest_framework.viewsets import ModelViewSet, GenericViewSet
from apps.students.models import Student, StudentSponsor
from apps.students.permissions import StudentPermission
from apps.students.serializers import (
    StudentSerializer,
    StudentListSerializer,
    StudentDetailSerializer,
    StudentSponsorSerializer,
    StudentSponsorUpdateSerializer
)
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentPermission]

    def get_serializer_class(self):
        if self.action == "list":
            return StudentListSerializer
        elif self.action == "retrieve":
            return StudentDetailSerializer
        return StudentSerializer


class StudentSponsorViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return StudentSponsorUpdateSerializer
        return StudentSponsorSerializer


