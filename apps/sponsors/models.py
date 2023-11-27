from apps.core.models import TimeStampedModel
from django.db import models
from apps.sponsors.choices import (
    SponsorType,
    SponsorStatus,
    SponsorPaymentType
)


class Sponsor(TimeStampedModel):
    full_name = models.CharField(max_length=250)
    type = models.CharField(max_length=50, choices=SponsorType.choices)
    phone_number = models.CharField(max_length=13)
    status = models.CharField(max_length=50, choices=SponsorStatus.choices, default=SponsorStatus.NEW)
    organization = models.CharField(max_length=125, null=True, blank=True)
    payment_amount = models.BigIntegerField(default=0)
    payment_type = models.CharField(max_length=50, choices=SponsorPaymentType.choices)

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"

    def __str__(self):
        return f"{self.full_name}"
