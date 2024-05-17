from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import C2BTransaction
from .serializers import C2BRegisterSerializer, C2BTransactionValidationResponseSerializer
import requests
from requests.auth import HTTPBasicAuth
import re

def generate_access_token():
    consumer_key = "gCJhB7ZOtowqVL2InVCFIWoZkZ7eU80RoBfrxG25gnp4OQ1L"
    consumer_secret = "id1Y393iO01xmjKKvqp2cT9ohzAKMP0SuOdGzfmjZVG8UCvXeNs9918ul2hmEz3k"

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        r = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()
        response_json = r.json()
        return response_json.get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Error generating access token: {e}")
        return None

class RegisterC2BUrl(APIView):
    def post(self, request):
        serializer = C2BRegisterSerializer(data=request.data)
        if serializer.is_valid():
            short_code = serializer.validated_data['short_code']
            response_type = serializer.validated_data['response_type']
            confirmation_url = serializer.validated_data['confirmation_url']
            validation_url = serializer.validated_data.get('validation_url', "")

            access_token = generate_access_token()
            if not access_token:
                return Response({'error': 'Failed to generate access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {
                "ShortCode": short_code,
                "ResponseType": response_type,
                "ConfirmationURL": confirmation_url,
                "ValidationURL": validation_url,
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error registering C2B URL: {e}")
                if response is not None and response.status_code is not None:
                    return Response({'error': f'API request failed with status code {response.status_code}'}, status=response.status_code)
                else:
                    return Response({'error': 'API request failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                originator_coversation_id = response.json().get('OriginatorCoversationID', None)
                if not originator_coversation_id:
                    return Response({'error': 'Missing OriginatorCoversationID in response'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                transaction = C2BTransaction.objects.create(
                    short_code=short_code,
                    response_type=response_type,
                    confirmation_url=confirmation_url,
                    validation_url=validation_url,
                    originator_coversation_id=originator_coversation_id
                )
                serializer = C2BRegisterSerializer(transaction)
                return Response({
                    "OriginatorCoversationID": transaction.originator_coversation_id,
                    "ResponseCode": "0",
                    "ResponseDescription": "Success"
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Error creating transaction: {e}")
                return Response({'error': 'Error creating transaction'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ValidationURL(APIView):
    def post(self, request):
        serializer = C2BTransactionValidationResponseSerializer(data=request.data)
        if serializer.is_valid():
            trans_id = serializer.validated_data.get('TransID')
            transaction_type = serializer.validated_data.get('TransactionType')
            trans_time = serializer.validated_data.get('TransTime')
            trans_amount = serializer.validated_data.get('TransAmount')
            business_short_code = serializer.validated_data.get('BusinessShortCode')
            bill_ref_number = serializer.validated_data.get('BillRefNumber')
            invoice_number = serializer.validated_data.get('InvoiceNumber')
            org_account_balance = serializer.validated_data.get('OrgAccountBalance')
            third_party_trans_id = serializer.validated_data.get('ThirdPartyTransID')
            msisdn = serializer.validated_data.get('MSISDN')
            first_name = serializer.validated_data.get('FirstName')
            middle_name = serializer.validated_data.get('MiddleName')
            last_name = serializer.validated_data.get('LastName')

            try:
                transaction = C2BTransaction.objects.get(trans_id=trans_id)
                if transaction.validation_response_sent:
                    return Response({'ResultCode': '0', 'ResultDesc': 'Already Validated'}, status=status.HTTP_200_OK)

                # Check if the transaction amount is less than 1 or greater than 1000000
                if float(trans_amount) < 1 or float(trans_amount) > 1000000:
                    validation_result = 'C2B00013'
                    validation_message = 'Rejected'
                    transaction.default_action = 'Cancelled'
                    transaction.save()
                # Check if the bill reference number is correct
                elif not re.match(r'^[A-Z0-9]{10}$', bill_ref_number):
                    validation_result = 'C2B00012'
                    validation_message = 'Rejected'
                    transaction.default_action = 'Cancelled'
                    transaction.save()
                # Check if the business short code is not 5 or 6 digits long
                elif not re.match(r'^[0-9]{5,6}$', business_short_code):
                    validation_result = 'C2B00015'
                    validation_message = 'Rejected'
                    transaction.default_action = 'Cancelled'
                    transaction.save()
                # Check if the transaction has already been cancelled
                elif transaction.default_action == 'Cancelled':
                    validation_result = 'C2B00016'
                    validation_message = 'Rejected'
                    transaction.default_action = 'Cancelled'
                    transaction.save()
                # Validate the transaction
                else:
                    validation_result = '0'
                    validation_message = 'Accepted'

                transaction.transaction_type = transaction_type
                transaction.trans_id = trans_id
                transaction.trans_time = trans_time
                transaction.trans_amount = trans_amount
                transaction.invoice_number = invoice_number
                transaction.org_account_balance = org_account_balance
                transaction.third_party_trans_id = third_party_trans_id
                transaction.msisdn = msisdn
                transaction.first_name = first_name
                transaction.middle_name = middle_name
                transaction.last_name = last_name
                transaction.validation_response_sent = True
                transaction.default_action = 'Completed' if validation_result == '0' else 'Cancelled'
                transaction.save()

                validation_response = {
                    "ResultCode": validation_result,
                    "ResultDesc": validation_message,
                }
                return Response(validation_response, status=status.HTTP_200_OK)

            except C2BTransaction.DoesNotExist:
                return Response({'ResultCode': 'C2B00012', 'ResultDesc': 'Rejected because transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
