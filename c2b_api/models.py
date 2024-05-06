from django.db import models

class C2BTransaction(models.Model):
    short_code = models.CharField(max_length=10)
    response_type = models.CharField(max_length=10, null=True, blank=True)
    confirmation_url = models.URLField(null=True, blank=True)
    validation_url = models.URLField(null=True, blank=True)
    command_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    msisdn = models.CharField(max_length=15, null=True, blank=True)
    bill_ref_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"C2B Transaction - Short Code: {self.short_code}"
