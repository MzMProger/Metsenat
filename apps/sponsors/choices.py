from django.db import models


class SponsorType(models.TextChoices):
    LEGAL_ENTITY = ("legal_entity", "Yuridik shaxs")
    INDIVIDUAL = ("individual", "Jismoniy shaxs")


class SponsorStatus(models.TextChoices):
    NEW = ("new", "Yangi")
    PENDING = ("pending", "Moderatsiyda")
    CONFIRMED = ("confirmed", "Tasdiqlangan")
    CANCELED = ("canceled", "Bekor qilingan")


class SponsorPaymentType(models.TextChoices):
    CASH = ("cash", "Naqd pul")
    TRANSFER = ("transfer", "Pul o'tkazmalari")
