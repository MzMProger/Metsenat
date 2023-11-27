from django.db import models


class StudentType(models.TextChoices):
    BACHELOR = ("bachelor", "Bakalavr")
    MASTER = ("master", "Magistr")