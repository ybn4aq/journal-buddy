from django.db.models import IntegerField, Model, models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Journal(models.Model):
    date = models.DateField
    content = models.CharField(max_length=500)
    rate = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    media = models.ImageField()

    def __str__(self):
        return "Date: " + self.date + "\nContent: " + self.content + "\nRate: " + self.rate