import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from users.models import CustomUser as User
import sys 
from datetime import datetime, timedelta, timezone 
from django.contrib.auth.decorators import login_required

#f = open(sys.path[0] + '\\moralis_api_key.json')
#data = json.loads(f.read())
#f.close()
from config import MORALIS_API_KEY

API_KEY = MORALIS_API_KEY['API_KEY']

if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit

def moralis_auth(request, *kwargs):
    return render(request, 'web3_auth/login_authentication.html', {})

@login_required()
def my_profile(request):
    return render(request, 'web3_auth/profile.html', {})

def request_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'

    #setting request expiration time to 1 minute after the present->
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'
    print(f'ExpirationTime = {expirationTime}')

    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})
    return JsonResponse(json.loads(x.text))

def verify_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))