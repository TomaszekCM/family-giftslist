from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MonthDayField(models.Field):
    """Custom field to store only month and day"""
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4  # Store as MMDD
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(4)'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        try:
            month = int(value[:2])
            day = int(value[2:])
            if 1 <= month <= 12 and 1 <= day <= 31:
                return {'month': month, 'day': day}
        except (ValueError, TypeError, IndexError):
            pass
        return None

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return None
        try:
            month = int(value[:2])
            day = int(value[2:])
            if 1 <= month <= 12 and 1 <= day <= 31:
                return {'month': month, 'day': day}
        except (ValueError, TypeError, IndexError):
            pass
        return None

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str) and len(value) == 4:
            return value
        if isinstance(value, dict):
            month = str(value['month']).zfill(2)
            day = str(value['day']).zfill(2)
            return f"{month}{day}"
        return None


class UserExt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = MonthDayField(verbose_name="Date of Birth")
    names_day = MonthDayField(verbose_name="Names Day", null=True, blank=True)
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
