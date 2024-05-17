from rest_framework import serializers
from .models import C2BTransaction

class C2BRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BTransaction
        fields = ['short_code', 'response_type', 'confirmation_url', 'validation_url']

class C2BTransactionValidationResponseSerializer(serializers.Serializer):
    TransactionType = serializers.CharField(max_length=50, required=True)
    TransID = serializers.CharField(max_length=50, required=True)
    TransTime = serializers.CharField(max_length=50, required=True)
    TransAmount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    ShortCode = serializers.CharField(max_length=50, required=True)
    BillRefNumber = serializers.CharField(max_length=50, required=True)
    InvoiceNumber = serializers.CharField(max_length=50, required=True)
    OrgAccountBalance = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    ThirdPartyTransID = serializers.CharField(max_length=50, required=True)
    MSISDN = serializers.CharField(max_length=50, required=True)
    FirstName = serializers.CharField(max_length=50, required=True)
    MiddleName = serializers.CharField(max_length=50, required=True)
    LastName = serializers.CharField(max_length=50, required=True)
