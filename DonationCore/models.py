from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


institutions = [
    ('1', 'fundacja'),
    ('2', 'organizacja pozarządowa'),
    ('3', 'zbiórka lokalna')
]


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(choices=institutions, default=1, max_length=100)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name, self.description}'


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField()
    phone_number = models.IntegerField()
    city = models.CharField()
    zip_code = models.CharField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

