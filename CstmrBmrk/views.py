from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated

from CstmrBmrk.factory import theBookmarkFactory,theCustomerFactory
from django.http.response import HttpResponse,JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json

class Customer(APIView):
    """ This class defines the Customer create,update """
    
    def post(self,request):
        resp=theCustomerFactory.create(request.data)
        if resp:
            return JsonResponse(resp)



class CustomerAuth(APIView):

    """ This class create token authentication for the customer to login for the bookmark etc., """

    permission_classes=[AllowAny]
    authentication_classes = (JSONWebTokenAuthentication,)
    
    def post(self,request):
        responseblock={}
        data =request.data
        username           =   data['username']
        password        =   data['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if request.user.is_authenticated:
                print (user.id)
            jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            temp_token = jwt_encode_handler(payload)
            token = "Bearer " + temp_token
            # print(token)
            responseblock['status']="success"
            responseblock['message']="successfully logged in"
            responseblock['token']=token
            response=JsonResponse(responseblock)
            
        else:
            responseblock['status']="failure"
            responseblock['message']="something went wrong"
            response=JsonResponse(responseblock)
        return response


class Bookmark(APIView):

    """ This class defines the Bookmark create """

    permission_classes=[IsAuthenticated]
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        payload = request.data
        customer_id=request.user.id
        resp = theBookmarkFactory.create(payload,customer_id)
        print("success")
        return JsonResponse({"message":"successfully bookmark created"})

class BookmarkFilter(APIView):

    """ This class defines the Bookmark Filter """


    def get(self,request):
        parameters = request.query_params
        resp = theBookmarkFactory.get_bookmark_filter(parameters)
        print(resp)
        return JsonResponse(resp,safe=False)
       





