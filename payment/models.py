from django.db import models
from django.utils import timezone

# Create your models here.
class Payment(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    organization = models.CharField()
    package = models.CharField()
    requests = models.CharField()
    paymentId = models.CharField()
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(default= timezone.now)

    def __str__(self):
        paid = "Paid" if self.paid else "Not paid"
        return f"{self.name}  ->  {paid}  ->  {self.date}"