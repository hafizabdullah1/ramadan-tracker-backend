from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    ramadan_start_date = models.DateField(default=date(2025, 3, 2))


class Activity(models.Model):
    PRAYER_CHOICES = [
        ("jamat", "Jamat/On Time"),
        ("late", "Late"),
        ("missed", "Missed"),
    ]

    ROZA_CHOICES = [
        ("kept", "Kept"),
        ("missed", "Missed"),
    ]

    SADQA_CHOICES = [
        ("given", "Given"),
        ("not_given", "Not Given"),
    ]

    TARAWEEH_CHOICES = [2, 4, 6, 8]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    fajr = models.CharField(max_length=10, choices=PRAYER_CHOICES, default="missed")
    zohar = models.CharField(max_length=10, choices=PRAYER_CHOICES, default="missed")
    asar = models.CharField(max_length=10, choices=PRAYER_CHOICES, default="missed")
    maghrib = models.CharField(max_length=10, choices=PRAYER_CHOICES, default="missed")
    isha = models.CharField(max_length=10, choices=PRAYER_CHOICES, default="missed")
    roza = models.CharField(max_length=10, choices=ROZA_CHOICES, default="missed")
    quran_pages = models.PositiveIntegerField(default=0)
    sadqa = models.CharField(max_length=10, choices=SADQA_CHOICES, default="not_given")
    taraweeh = models.PositiveIntegerField(
        choices=[(choice, choice) for choice in TARAWEEH_CHOICES], default=0
    )
    extra_good_deeds = models.BooleanField(default=False)
    ramadan_day = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_points(self):
        points = 0
        points += {"jamat": 10, "late": 5, "missed": 0}.get(self.fajr, 0)
        points += {"jamat": 10, "late": 5, "missed": 0}.get(self.zohar, 0)
        points += {"jamat": 10, "late": 5, "missed": 0}.get(self.asar, 0)
        points += {"jamat": 10, "late": 5, "missed": 0}.get(self.maghrib, 0)
        points += {"jamat": 10, "late": 5, "missed": 0}.get(self.isha, 0)
        points += 10 if self.roza == "kept" else 0
        points += self.quran_pages
        points += self.taraweeh * 2
        points += 5 if self.sadqa == "given" else 0
        points += 2 if self.extra_good_deeds else 0
        return points

    def save(self, *args, **kwargs):
        # Ramadan Day Calculation
        print("ramadan_day outside of if", self.ramadan_day)
        if not self.ramadan_day:
            print("ramadan_day in if part", self.ramadan_day)
            self.ramadan_day = (date.today() - self.user.ramadan_start_date).days + 1

        # Restricting activities beyond 30 days
        if self.ramadan_day > 30:
            raise ValueError("Ramadan activities can only be logged for 30 days.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
