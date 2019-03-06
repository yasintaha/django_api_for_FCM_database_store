from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import ReportSerializer
import pyrebase

#FCM credentials
config = {
    "apiKey" : "<api_key>",
    "authDomain" : "<auth_Domain>",
    "databaseURL" : "<database_URL>",
    "projectId" : "<project_Id>",
    "storageBucket" : "<storage_Bucket>",
    "messagingSenderId" : "<messaging_SenderId>"
  }

# firebase = pyrebase.initialize_app(config)
firebase = pyrebase.initialize_app(config)

# for FCM authentication like login,signup and get_account_info
authe = firebase.auth()

# for database storage of FCM
database = firebase.database()

class ReportView(APIView):
    serializer_class = ReportSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # FCM registered or signed up user email and password
            email = serializer.data['email']
            password = serializer.data['password']
            try:
                # logging in user to fetch idToken 
                user = authe.sign_in_with_email_and_password(email,password)

                # print(user)
                user_fcm_token = user['idToken']

            except:
                print('------------')

            work_assigned = serializer.data['work_assigned']
            progress = serializer.data['progress']

            # getting the users account_info by user "idToken" which is initialized in the above try block.
            a = authe.get_account_info(user_fcm_token)
            user_dict = a['users']  #users dictonaries values from FCM

            user_index_for_localId = user_dict[0] #users index value
            user_localId = user_index_for_localId['localId'] #initializing the localId from user_dict
            b = user_localId

            data = {
                'work_assigned':work_assigned,
                'progress':progress
            }
            #storing value in FCM database 
            database.child('users').child(b).child('reports').set(data)
            content = {'message':'Values are stored in FCM database'}
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            # content = {'message':'Unable to store value'}
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
