from django.db import models

class Name(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)
class Item(models.Model):
    price = models.IntegerField()
    names = models.ManyToManyField(Name)
    def __str__(self):
        return self.price
    class Meta:
        ordering = ('price',)