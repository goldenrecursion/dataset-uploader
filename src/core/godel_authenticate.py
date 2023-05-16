
from godel import GoldenAPI

def retrieve_signable_message(user_wallet_address):
    USER_ID = user_wallet_address
    API_URL = "https://dapp.golden.xyz/graphql"
    SANDBOX_URL = "https://sandbox.dapp.golden.xyz/graphql" # Use the sandbox API to test your submissions
    goldapi = GoldenAPI(url=API_URL)

    # Retrieve one-off nonce from GraphQL API
    message_response = goldapi.get_authentication_message(user_id=USER_ID)
    message_response

    # Sign and verify nonce with your wallet's private key (KEEP THIS SECURE)
    message_string = message_response["data"]["getAuthenticationMessage"]["string"]
    print(f'godel authentication message to sign: "{message_string}"')
    return str(message_string) 

def retrieve_jwt(user_wallet_address, signature):
    print('Checkpoint: retrieve_jwt')
    USER_ID = user_wallet_address 

    API_URL = "https://dapp.golden.xyz/graphql"
    SANDBOX_URL = "https://sandbox.dapp.golden.xyz/graphql" # Use the sandbox API to test your submissions
    goldapi = GoldenAPI(url=API_URL)
    print(f'Checkpoint: goldapi initialized with API_URL')

    # Authenticate with Golden's API and you'll receive a jwt bearer token
    auth_response = goldapi.authenticate(
        user_id=USER_ID,
        signature=signature
    )
    
    print(f'Checkpoint: jwt token retrieved from goldapi')
    jwt_token = auth_response["data"]["authenticate"]["jwtToken"]

    # Set JWT token to verify your wallet/role and unlock permissions to the rest of the API
    goldapi.set_jwt_token(jwt_token=jwt_token)

    print("Your JWT Token:\n", jwt_token)
    return jwt_token

def authenticate_with_jwt(jwt):
    try:
        API_URL = "https://dapp.golden.xyz/graphql"
        SANDBOX_URL = "https://sandbox.dapp.golden.xyz/graphql" # Use the sandbox API to test your submissions
        goldapi = GoldenAPI(url=API_URL)
        goldapi.set_jwt_token(jwt_token=jwt)
        print(f'Successfully authenticated Golden API with Godel (Backend)')
        return True #Return True if successfully authenticated with this jwt
    except Exception as e:
        print(f'Exception: \n{e}')
        return False #Return False if authentication failed with this jwt

#def authenticate_with_jwt_and_do_something_with_the_api(jwt):
#   placeholder for utility function:
#       disambiguation, 
#       uploading, 
#       checking statuses, 
#       etc. 