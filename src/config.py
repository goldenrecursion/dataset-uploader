#configuration stuff 
#WARNING: Keep sensitive data (like secret key) secret
import json

secret_key_file = open("secret_key.txt", "r")
SECRET_KEY = secret_key_file.read()
secret_key_file.close()

api_key_file = open("moralis_api_key.json", "r")
MORALIS_API_KEY = json.loads(api_key_file.read())
api_key_file.close()
