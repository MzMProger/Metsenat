from apps.sponsors.choices import SponsorType
from apps.sponsors.models import Sponsor
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class SponsorListSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField("get_spent_amount", read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            "id",
            "full_name",
            "phone_number",
            "payment_amount",
            "spent_amount",
            "created_at",
            "status",
        ]

    def get_spent_amount(self, obj):
        return 0


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "id",
            "full_name",
            "phone_number",
            "payment_amount",
            "organization",
            "type",
            "status",
            "created_at",
        ]


class SponsorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        exclude = [
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if attrs.get("type") == SponsorType.LEGAL_ENTITY.value:
            if not attrs.get("organization"):
                raise ValidationError(
                    f"Organization is required when sponsor type is {SponsorType.LEGAL_ENTITY.value}"
                )
        elif attrs.get("type") == SponsorType.INDIVIDUAL.value:
            attrs["organization"] = None
        return attrs


class SponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        exclude = [
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if attrs.get("type") == SponsorType.LEGAL_ENTITY.value:
            if not attrs.get("organization"):
                raise ValidationError(
                    f"Organization is required when sponsor type is {SponsorType.LEGAL_ENTITY.value}"
                )
        elif attrs.get("type") == SponsorType.INDIVIDUAL.value:
            attrs["organization"] = None
        return attrs
