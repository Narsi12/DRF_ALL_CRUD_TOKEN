# class AuthenticateUser(APIView):#Working man
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
#             'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
#         }
#     ))
#     def post(self, request, format=None):
#         # import pdb;pdb.set_trace()
#         data = json.loads(request.body)
#         user = USER_details.objects.filter(Q(email__iexact=data["email"])).first()
#         if user is not None:
#             encrypted_password = user.password  
#             decrypted_password = decrypt(bytes(encrypted_password, "utf-8"), SECRET_KEY.encode()).decode()  
#             x= decrypted_password 
#             if x == data["password"]:  
#                 token_payload = {
#                     'user_id': user.id,
#                     'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION)
#                      }  
#                 access_token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

#                 refresh_token_payload = {
#                     'user_id': user.id,
#                     'exp': datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRATION)
#                     }
#                 refresh_token = jwt.encode(refresh_token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

#                 mycol.insert_one({
#                      "user_id": user.id,
#                      "token": access_token,
#                      })
#                 return JsonResponse({"status": "success", "msg": "user successfully authenticated", "token": access_token,"refresh_token":refresh_token})
#             else:
#                 return JsonResponse({"status": "error", "msg": "incorrect password"})
#         else:
#             return JsonResponse({"status": "error", "msg": "incorrect email"})


# settings.py
# # Generate a secure random string for JWT secret key
# JWT_SECRET_KEY = secrets.token_hex(32)

# JWT_ACCESS_TOKEN_EXPIRATION = 60
# JWT_REFRESH_TOKEN_EXPIRATION = 1440 # 1 day
# JWT_AUTH_HEADER_PREFIX = 'Bearer'
# # Define the JWT secret key and algorithm
# JWT_SECRET_KEY = 'your_secret_key'
# JWT_ALGORITHM = 'HS256'

SECRET_KEY = 'SECRET_KEY'
import jwt
# DECODING THE TOKEN 
def validate_token(access_token):
    try:
        # Decode the token, using the same secret key used to sign it
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        # If the token was successfully decoded, return the payload
        return payload
    except jwt.ExpiredSignatureError:
        # If the token has expired, raise an exception
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        # If the token is invalid, raise an exception
        raise Exception('Invalid token')
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxODk2MTc2LCJpYXQiOjE2ODE4OTU4NzYsImp0aSI6IjhjZmQ2YWQ5ZjczODQ2ODY4ZTQzM2NjNmY5ZDJlMDk0IiwidXNlcl9pZCI6M30.g-DS-nPapKekdkEDc8hlaM0kyoONJNkuMwxYjP7eWT8'
payload = validate_token(access_token)
print(payload)