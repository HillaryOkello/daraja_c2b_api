from rest_framework import serializers
from .models import C2BTransaction

class C2BRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BTransaction
        fields = ['short_code', 'response_type', 'confirmation_url', 'validation_url']

class C2BTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BTransaction
        fields = ['short_code', 'command_id', 'amount', 'msisdn', 'bill_ref_number']
