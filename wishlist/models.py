from django.db import models
from django.contrib.auth.models import User


class UserExt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name="Date of Birth")
    names_day = models.DateField(verbose_name="Names Day", null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class ImportantDates(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(verbose_name="Date")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Gift(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('average', 'Average'),
        ('low', 'Low'),
    ]

    who_wants_it = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wanted_gifts")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='average')
    approx_price = models.PositiveIntegerField()
    reserved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="reserved_gifts")
    link_to_shop = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.who_wants_it.first_name} {self.who_wants_it.last_name})"
