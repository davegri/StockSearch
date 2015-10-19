from django.db import models

# Create your models here.
class SearchQuery(models.Model):
    text = models.CharField(max_length=400)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.text