from rest_framework.routers import DefaultRouter
from apps.students.views import StudentViewSet, StudentSponsorViewSet


router = DefaultRouter()
router.register("students", StudentViewSet, basename="students")
router.register("student_sponsors", StudentSponsorViewSet, basename="student_sponsors")

urlpatterns = router.urls
