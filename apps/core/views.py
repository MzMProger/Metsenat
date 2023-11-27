# 1. Total students' allocated amount
# 2. Total students' contract amount
# 3. Contract amount that should be payed
import datetime

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.sponsors.choices import SponsorStatus
from apps.sponsors.models import Sponsor
from apps.students.models import StudentSponsor, Student
from rest_framework.viewsets import GenericViewSet


class DashboardViewSet(GenericViewSet):
    @action(methods=["GET"], detail=False)
    def chart_one(self, request, *args, **kwargs):
        total_allocated_amount = StudentSponsor.objects.aggregate(
            total_allocated_amount=Sum("allocated_amount")
        ).get("total_allocated_amount")
        total_contract_amount = Student.objects.aggregate(
            total_contract_amount=Sum("contract_amount")
        ).get("total_contract_amount")

        data = {
            "total_allocated_amount": total_allocated_amount,
            "total_contract_amount": total_contract_amount,
            "left_contract_amount": total_contract_amount - total_allocated_amount
        }
        return Response(data)

    @action(methods=["GET"], detail=False)
    def chart_two(self, request, *args, **kwargs):
        students = {
            s.get("date").strftime("%Y-%m-%d"): s.get("count") for s in Student.objects.annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('date')
        }
        sponsors = {
            s.get("date").strftime("%Y-%m-%d"): s.get("count") for s in Sponsor.objects.filter(status=SponsorStatus.CONFIRMED).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        }

        students = self.get_data_for_all_days(students)
        sponsors = self.get_data_for_all_days(sponsors)

        data = {
            "students": students,
            "sponsors": sponsors,
        }
        return Response(data)

    def get_data_for_all_days(self, objects):
        today = timezone.now()
        for i in range(366):
            target_date = today - datetime.timedelta(days=i)
            if target_date.strftime("%Y-%m-%d") not in objects:
                objects[target_date.strftime("%Y-%m-%d")] = 0
        return objects

