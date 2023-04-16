from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee,USER_details
from .serializers import EmployeeSerializer,USER_Serializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import generics,mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Q 
import json
from django.core.mail import EmailMessage
from smtplib import SMTPRecipientsRefused
from drf_yasg.utils import swagger_auto_schema
from .encryptdecrypt import encrypt,decrypt
from pymongo import MongoClient
import datetime
client = MongoClient('mongodb://localhost:27017')
SECRET_KEY='1234567'

#Function-Based 
@api_view(['GET'])
def all_details(request,pk=None):
    id=pk
    if id is not None:
        try:
            employees=Employee.objects.get(id=pk)
            serializer=EmployeeSerializer(employees)
            return Response(serializer.data)
        except employees.DoesNotExist:
            return Response({'Message':'Data not found '}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        employees=Employee.objects.all()
        serializer=EmployeeSerializer(employees, many=True)
        return Response({'status':200, 'payload':serializer.data})

@api_view(['POST'])
def create_data(request):
    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PUT'])
def update_data(request,pk):
    employees=Employee.objects.get(id=pk) 
    serializer=EmployeeSerializer(employees,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response( serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def delete_data(request,pk):
    employee=Employee.objects.get(id=pk)
    employee.delete()
    return Response({"Messgae":"Employee deleted "})


#Class Based 
class classBased(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    def get(self, request, pk=None , format=None):
        if pk is not None:
            try:
                employee = Employee.objects.get(id=pk)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response({'Message':"Data is not found "})
        else:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response( serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data)
        return Response({'status': 400, 'payload': serializer.errors})

    def put(self, request, pk):
        employee = Employee.objects.get(id=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'payload': serializer.data})
        return Response({'status': 400, 'payload': serializer.errors})

    def delete(self, request, pk):
        employee = Employee.objects.get(id=pk)
        employee.delete()
        return Response({'status': "DELETED SUCESSFULLY"})


# mixins crud
class EmployeelistCreateApiView(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class EmployeeRetriveUpdateDeleteApiView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


#Generic crud
class empPost(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class empget(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



# Viewsets

class employeeView(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset,many=True)
        return Response(serializer.data)
    def create(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def retrieve(self,request,pk=None):
        queryset = Employee.objects.all()
        data_id = get_object_or_404(queryset,pk=pk)
        serializer = EmployeeSerializer(data_id)
        return Response(serializer.data)
    def update(self,request,pk=None):
        queryset = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def partial_update(self,request,pk=None):
        queryset = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def destroy(self,request,pk=None):
        queryset = Employee.objects.get(pk=pk)
        queryset.delete()
        return Response({"Message":"Record Deleted Sucessfully"})
    

# Mail sending format
class mailsender(APIView):
    def post(self,request):
        email = request.data.get('email')
        subject = request.data.get('subject')
        body = request.data.get('body')

        try:
            sending = EmailMessage(
                subject=subject,
                body=body,
                to = [email]
            )
            sending.send()
        except SMTPRecipientsRefused:
            return Response({'error':'Invalid email address'})
        return Response({'message':'Email sent Successfully'})


#USer Signup
class Signup(APIView):
    @swagger_auto_schema(
         operation_id='Sign up',
         request_body=USER_Serializer)
    
    def post(self, request, format=None):
        serializer = USER_Serializer(data=json.loads(request.body))
        if serializer.is_valid():
            data = serializer.validated_data
            password = data['password']
            password = encrypt(bytes(password, "utf-8"), SECRET_KEY.encode()).decode()
            data['password'] = password
            email = data['email']
            existing_user = USER_details.objects.filter(email=email).first()
            if existing_user is not None:
                return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return JsonResponse({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'Message': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)


#Token Generations
db = client['token']
mycol = db["tokenDB"]      
class AuthenticateUser(APIView):#Working man
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
        }
    ))
    def post(self, request, format=None):
        # import pdb;pdb.set_trace()
        data = json.loads(request.body)
        user = USER_details.objects.filter(Q(email__iexact=data["email"])).first()
        if user is not None:
            encrypted_password = user.password
            decrypted_password = decrypt(bytes(encrypted_password, "utf-8"), SECRET_KEY.encode()).decode()
            x= decrypted_password
            if x == data["password"]:
                token, created = Token.objects.get_or_create(user_id=user.id)
                mycol.insert_one({
                    "user_id": str(user.id),
                    "token": token.key,
                    "created_at": datetime.datetime.now()
                    })
                return JsonResponse({"status": "success", "msg": "user successfully authenticated", "token": token.key})
            else:
                return JsonResponse({"status": "error", "msg": "incorrect password"})
        else:
            return JsonResponse({"status": "error", "msg": "incorrect email"})