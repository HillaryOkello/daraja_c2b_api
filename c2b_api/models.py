from django.db import models
from django.utils import timezone

class C2BTransaction(models.Model):
    short_code = models.CharField(max_length=10)
    response_type = models.CharField(max_length=10, null=True, blank=True)
    confirmation_url = models.URLField(null=True, blank=True)
    validation_url = models.URLField(null=True, blank=True)
    command_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    msisdn = models.CharField(max_length=15, null=True, blank=True)
    bill_ref_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    originator_coversation_id = models.CharField(max_length=36, unique=True, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, null=True, blank=True)
    trans_id = models.CharField(max_length=36, null=True, blank=True)
    trans_time = models.DateTimeField(null=True, blank=True)
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True),
    invoice_number = models.CharField(max_length=50,null=True, blank=True)
    validation_response_sent = models.BooleanField(default=False, null=True, blank=True)
    default_action = models.CharField(max_length=10, choices=[('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Completed')
    created_at = models.DateTimeField(default=timezone.now)
    org_account_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    third_party_trans_id = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"C2B Transaction - Short Code: {self.short_code}"
