from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(help_text="Price in TZS")

    def __str__(self):
        return self.name


class PaymentPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weekly_contribution = models.PositiveIntegerField(default=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def total_saved(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def target_amount(self):
        return self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Payment(models.Model):
    plan = models.ForeignKey(PaymentPlan, related_name='payments', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan.user.username} paid {self.amount} TZS on {self.paid_at.date()}"


