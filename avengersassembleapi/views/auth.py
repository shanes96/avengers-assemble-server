from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash
from avengersassembleapi.models import AvengerUser
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

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


def add_subscriber_to_mailchimp(email):
    client = MailChimp(mc_api='5eda1bb3ed659f9cdb147fabc067cc91-us21', mc_user='shanestandifur@gmail.com')
    list_id = '2da45402b8'
    email_hash = get_subscriber_hash(email)
    data = {
        'email_address': email,
        'status': 'subscribed'
    }
    client.lists.members.create(list_id=list_id, data=data)

@ensure_csrf_cookie
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    csrf_token = get_token(request)
    
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email= request.data['email']
    )

    avenger = AvengerUser.objects.create(
        user=new_user
    )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=avenger.user)
    mailchimp_url = "https://<datacenter>.api.mailchimp.com/3.0/lists/2da45402b8/members"
    mailchimp_data = {
        "email_address": new_user.email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": new_user.first_name,
            "LNAME": new_user.last_name
        }
    }
    MAILCHIMP_API_KEY = '5eda1bb3ed659f9cdb147fabc067cc91-us21'
    mailchimp_auth = ("", MAILCHIMP_API_KEY)

    response = requests.post(mailchimp_url, json=mailchimp_data, auth=mailchimp_auth)

    # Return the token to the client
    data = { 'token': token.key }
    response['X-CSRFToken'] = csrf_token
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    return Response(data)
