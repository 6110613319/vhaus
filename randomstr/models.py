from django.db import models

# Create your models here.
# เก็บstring
class StoreString(models.Model):
    randomStr = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.randomStr}"