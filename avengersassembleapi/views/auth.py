from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed, JsonResponse
import requests
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from avengersassembleapi.models import AvengerUser
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
import json

CORS_ORIGIN_WHITELIST = [    "http://localhost:3000",    "http://127.0.0.1:3000"]


@api_view(['POST'])
@permission_classes([AllowAny])

def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password,)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'id':authenticated_user.id,
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])


@csrf_exempt
@ensure_csrf_cookie
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    
    if request.method == 'POST':
        # get JSON data from request body
        data = json.loads(request.body)
        
        # create new user with data
        new_user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )

        avenger = AvengerUser.objects.create(
            user=new_user
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=avenger.user)
        mailchimp_url = "https://us21.api.mailchimp.com/3.0/lists/AUDIENCE_ID/members"
        mailchimp_data = {
            "email_address": new_user.email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": new_user.first_name,
                "LNAME": new_user.last_name
            }
        }
        MAILCHIMP_API_KEY = 'Mailchimp API Key Goes Here'
        mailchimp_auth = ("", MAILCHIMP_API_KEY)

        response = requests.post(mailchimp_url, json=mailchimp_data, auth=mailchimp_auth)

        # Return the token to the client
        # token = Token.objects.create(user=new_user)
        token = Token.objects.filter(user=new_user).first()
        if token:
            # If a token exists, delete it to create a new one
            token.delete()
        # Create a new token for the user
        token = Token.objects.create(user=new_user)
        response = JsonResponse({'token': token.key})
        response['X-CSRFToken'] = get_token(request)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    else:
        return HttpResponseNotAllowed(['POST'])