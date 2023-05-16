from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from . import godel_authenticate 
import json
from users.models import CustomUser

def truncate_user_address(current_user_address):
    truncated_user_address = current_user_address[:5] + '...' + current_user_address[-4:]
    return truncated_user_address

def check_jwt_validity(token):
    #check if this jwt enables a successful connection to the Golden API->
    validity_result = godel_authenticate.authenticate_with_jwt(token)
    return validity_result
 
@login_required()
def index(request):
    #extract the jwt from the extended User model. It'll either be a correct JWT, not exist(=NULL),
    #or an incorrect one. If NULL, pass a default value "None" to the template as context.
    
    current_user_address = request.user.username
    truncated_user_address = truncate_user_address(str(current_user_address))
    current_user_jwt = request.user.godel_jwt

    print(f'Checkpoint: index view')
    message = godel_authenticate.retrieve_signable_message(current_user_address)
    #note: Message is signed on the frontend, with ethers.js and Metamask's personal_sign(), formatted
    #per EIP-191 standards (akin to web3.py's eth.sign_message() in Godel's docs)    

    if current_user_jwt=="None":
        context = {'message':str(message),
                'truncated_user_address':str(truncated_user_address),
                'current_user_jwt':current_user_jwt,
                'jwt_validity_result':'N/A',} 
    else:
        #for backend jwt validity check: check jwt validity and send status to the frontend->
        token_is_valid = check_jwt_validity(current_user_jwt)
        if token_is_valid: #converting 'True' boolean to 'true' string for javascript
            jwt_validity = 'true'
        else:
            jwt_validity = 'false'
        context = {'message':str(message),
                'truncated_user_address':str(truncated_user_address),
                'current_user_jwt':current_user_jwt,
                'jwt_validity':jwt_validity,} 
    return render(request, 'core/index.html', context)

@login_required()
def authenticate_godel_with_signature(request):
    data = json.loads(request.body)
    print(data)
    signature = data['signature']
    current_user_address = request.user.username
    token = godel_authenticate.retrieve_jwt(current_user_address, signature)
    context = {'jwt_token':token}
    return JsonResponse(context)

@login_required()
def update_user_jwt(request):
    data = json.loads(request.body)
    print(data)
    token = data['jwt']
    current_user_address = request.user.username

    current_user = CustomUser.objects.get(username=current_user_address)
    print(f'(Before): Current User jwt = \n{current_user.godel_jwt}')
    current_user.godel_jwt = token
    print(f'(After): Current User jwt = \n{current_user.godel_jwt}')
    current_user.save()
    print(f'New jwt for user {current_user_address} saved')

    context = {'jwt_saved':True}
    return JsonResponse(context)
    #an alternative here is to redirect to index for changes to come into effect, but currently set to a 
    #manual reload from frontend with location.reload()
 
@login_required()
def upload_page(request):
    context = {}
    return render(request, 'core/upload_page.html', context)

