"""
WSGI config for narsimha project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narsimha.settings')

application = get_wsgi_application()




# refresh_token_schema = openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     required=['refresh', 'access'],
#     properties={
#         'refresh': openapi.Schema(type=openapi.TYPE_STRING),
#         'access': openapi.Schema(type=openapi.TYPE_STRING),
#     },
# )
# class RefreshTokenView(APIView):
#     # permission_classes = [IsAuthenticated]
#     @swagger_auto_schema(
#         operation_id='Refresh Token',
#         request_body=refresh_token_schema,
#         responses={200: 'OK', 400: 'Bad Request'},
#         security=[],
#     )
#     def post(self, request):
#         refresh_token = request.data.get('refresh')
#         access_token = request.data.get('access')
        
#         if refresh_token and access_token:
#             try:
#                 RefreshToken(refresh_token)
#                 new_access_token = str(RefreshToken(access_token).access_token)
#                 return Response({'access': new_access_token}, status=status.HTTP_200_OK)
#             except TokenError:
#                 pass
        
#         return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)