from django.db import models
from apps.core.models import TimeStampedModel
from apps.sponsors.models import Sponsor
from apps.students.choices import StudentType


class Student(TimeStampedModel):
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13, default="")
    type = models.CharField(max_length=50, choices=StudentType.choices)
    institute = models.CharField(max_length=125)
    contract_amount = models.BigIntegerField(default=0)
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name="students",
        through="students.StudentSponsor"
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.full_name}"


class StudentSponsor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT)
    allocated_amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
