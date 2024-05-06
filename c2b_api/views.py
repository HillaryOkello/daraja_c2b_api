from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import C2BTransaction
from .serializers import C2BRegisterSerializer, C2BTransactionSerializer
import requests
from requests.auth import HTTPBasicAuth

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
                transaction = C2BTransaction.objects.create(
                    short_code=short_code,
                    response_type=response_type,
                    confirmation_url=confirmation_url,
                    validation_url=validation_url
                )
                serializer = C2BRegisterSerializer(transaction)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Error creating transaction: {e}")
                if response is not None and response.status_code is not None:
                    return Response({'error': f'API request failed with status code {response.status_code}'}, status=response.status_code)
                else:
                    return Response({'error': 'API request failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SimulateC2BTransaction(APIView):
    def post(self, request):
        serializer = C2BTransactionSerializer(data=request.data)
        if serializer.is_valid():
            short_code = serializer.validated_data['short_code']
            command_id = serializer.validated_data['command_id']
            amount = serializer.validated_data['amount']
            msisdn = serializer.validated_data['msisdn']
            bill_ref_number = serializer.validated_data['bill_ref_number']

            if not short_code or not command_id or not amount or not msisdn or not bill_ref_number:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            access_token = generate_access_token()
            if not access_token:
                return Response({'error': 'Failed to generate access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            url = " https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {
                "ShortCode": short_code,
                "CommandID": command_id,
                "Amount": float(amount),
                "Msisdn": msisdn,
                "BillRefNumber": bill_ref_number
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error simulating C2B transaction: {e}")
                if response is not None and response.status_code is not None:
                    return Response({'error': f'API request failed with status code {response.status_code}'}, status=response.status_code)
                else:
                    return Response({'error': 'API request failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(response.json(), status=status.HTTP_200_OK)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ValidateC2BTransaction(APIView):
    def post(self, request):
        serializer = C2BTransactionSerializer(data=request.data)
        if serializer.is_valid():
            pass
