from apps.students.models import Student, StudentSponsor
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class StudentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField("get_created_at")

    class Meta:
        model = Student
        fields = "__all__"

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")


class StudentListSerializer(serializers.ModelSerializer):
    allocated_amount = serializers.SerializerMethodField("get_allocated_amount")

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "type",
            "institute",
            "allocated_amount",
            "contract_amount"
        ]

    def get_allocated_amount(self, obj):
        allocated_amount = get_student_allocated_amount(obj)
        return allocated_amount


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "full_name",
            "phone_number",
            "institute",
            "contract_amount"
        ]


class NestedStudentSponsorSerializer(serializers.ModelSerializer):
    sponsor_id = serializers.CharField(source="sponsor.id", read_only=True)
    sponsor_name = serializers.CharField(source="sponsor.full_name", read_only=True)

    class Meta:
        model = StudentSponsor
        fields = [
            "id",
            "sponsor_id",
            "sponsor_name",
            "allocated_amount"
        ]


class StudentDetailSerializer(serializers.ModelSerializer):
    sponsors = serializers.SerializerMethodField("get_sponsors")
    allocated_amount = serializers.SerializerMethodField("get_allocated_amount")

    class Meta:
        model = Student
        fields = "__all__"

    def get_sponsors(self, obj):
        queryset = StudentSponsor.objects.filter(student=obj)
        serializer = NestedStudentSponsorSerializer(queryset, many=True)
        return serializer.data

    def get_allocated_amount(self, obj):
        allocated_amount = get_student_allocated_amount(obj)
        return allocated_amount


class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = "__all__"

    def validate(self, attrs):
        stud_alloc_amount = get_student_allocated_amount(attrs.get("student"))
        if stud_alloc_amount + attrs.get("allocated_amount") > attrs.get("student").contract_amount:
            raise ValidationError(
                "Spent money more than student's contact amount!"
            )

        spon_alloc_amount = get_sponsor_allocated_amount(attrs.get("sponsor"))
        if spon_alloc_amount + attrs.get("allocated_amount") > attrs.get("sponsor").payment_amount:
            raise ValidationError(
                "Sponsor does not have enough money to be a this student's sponsor!"
            )

        if attrs.get("sponsor").status != "confirmed":
            raise ValidationError("Invalid sponsor!")

        return attrs


class StudentSponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = [
            "sponsor",
            "allocated_amount"
        ]

    def validate(self, attrs):
        stud_alloc_amount = get_student_allocated_amount(self.instance.student)
        if stud_alloc_amount + attrs.get(
                "allocated_amount",
                self.instance.allocated_amount
        ) > self.instance.student.contract_amount:
            raise ValidationError(
                "Total allocated amount must be lower or equal to contract amount of the student!"
            )

        spon_alloc_amount = get_sponsor_allocated_amount(attrs.get("sponsor"))
        if spon_alloc_amount + attrs.get(
                "allocated_amount",
                self.instance.allocated_amount
        ) > attrs.get("sponsor").payment_amount:
            raise ValidationError(
                "Not enough money to be the student's sponsor!"
            )
        return attrs


def get_student_allocated_amount(student):
    result = StudentSponsor.objects.filter(
        student=student
    ).aggregate(
        Sum("allocated_amount")
    ).get("allocated_amount__sum")
    if result is None:
        return 0
    return result


def get_sponsor_allocated_amount(sponsor):
    result = StudentSponsor.objects.filter(
        sponsor=sponsor
    ).aggregate(
        Sum("allocated_amount")
    ).get("allocated_amount__sum")
    if result is None:
        return 0
    return result
