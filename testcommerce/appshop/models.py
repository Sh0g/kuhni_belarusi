from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=100)
    prices=models.IntegerField()
    description=models.CharField(max_length=100)
    image=models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.name