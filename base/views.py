## Django imports
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
import pyrebase


from django.contrib.auth.models import User
from .models import User_profile

import json


from django.views.decorators.csrf import csrf_exempt
import uuid



## DRF imports
from rest_framework.decorators import api_view
from rest_framework.response import Response


# decorators
from .firebaseTokenSerializator import firebase_token_verification

# Create your views here.
@api_view(['GET','POST'])
def home(request):
    data = request.body
    return Response({"skuska":"working..","data":data})


@api_view(['POST'])
def registration_view(request):
      
    if request:
        user = User.objects.create_user(username=request.data['username'],
        password = request.data['password'],email=request.data['email'])
        user.save()
    else:
        return Response({"Error":"Something goes wrong..."})
  
        


    return Response({"Success":"User is sucessfully registrated!"})


###############################################################





@api_view(['POST'])
def fb_registration_view(request):
    firebaseConfig = {
    "apiKey": "AIzaSyAqYEbX3wP8cMWpp3LYrJnmlnoiUoAhzbc",
    "authDomain": "st-project-62715.firebaseapp.com",
    "projectId": "st-project-62715",
    "storageBucket": "st-project-62715.appspot.com",
    "messagingSenderId": "771921370520",
    "appId": "1:771921370520:web:6fda1cd80a2785b7fe5fed",
    "measurementId": "G-1G83VXG6Z5",
    "databaseURL": ""
    }
    firebase=pyrebase.initialize_app(firebaseConfig)
    authe = firebase.auth()
    #database=firebase.database()    

    """
    [{
        "pass":"skuska",
        "email":"skuska@skuska.com"
    }]
    """

    email=json.loads(request.body.decode())[0]["email"] or request.POST.get("email") 
    pasw=json.loads(request.body.decode())[0]["pass"] or request.POST.get("pass") 

    print(email,pasw)


    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return Response({"message":message})

    session_id=user['idToken']
    request.session['uid']=str(session_id)

    return Response({"user":user['idToken'],"email":email,"user_info":user})




"""
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html")
     return render(request,"Login.html")

"""

@api_view(['POST'])
def pure_fb_registration_view(request):
    pass

"""

# https://firebase.google.com/docs/auth/admin/create-custom-tokens#python

    #import os
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds.json"

    firebaseConfig = {
    "apiKey": "AIzaSyAqYEbX3wP8cMWpp3LYrJnmlnoiUoAhzbc",
    "authDomain": "st-project-62715.firebaseapp.com",
    "projectId": "st-project-62715",
    "storageBucket": "st-project-62715.appspot.com",
    "messagingSenderId": "771921370520",
    "appId": "1:771921370520:web:6fda1cd80a2785b7fe5fed",
    "measurementId": "G-1G83VXG6Z5",
    "databaseURL": ""
    }
    

    options = {
        'serviceAccountId': 'tPerULojkdSWNFVSJvQtnv9BcXh2@st-project-62715.iam.gserviceaccount.com',
    }
    
   

    fb=firebase_admin.initialize_app(options=firebaseConfig)
    fb.get_credentials()
    
    
    uid = str(uuid.uuid4())
    additional_claims = {
        "premiumAccount": True,
        "name":"skuska"
    }


    
    custom_token = auth.create_custom_token(uid, additional_claims,app=fb)
     
    return Response({"custom_token":"asc"})
"""



########################################################################
################################ FIREBASE ##############################
########################################################################
firebaseConfig = {
    "apiKey": "AIzaSyAqYEbX3wP8cMWpp3LYrJnmlnoiUoAhzbc",
    "authDomain": "st-project-62715.firebaseapp.com",
    "projectId": "st-project-62715",
    "storageBucket": "st-project-62715.appspot.com",
    "messagingSenderId": "771921370520",
    "appId": "1:771921370520 :web:6fda1cd80a2785b7fe5fed",
    "measurementId": "G-1G83VXG6Z5",
    "databaseURL": ""
    }

firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()




"""  register_user testing 
{
"username":"username1",
"email":"skuska@skuska.com",
"password":"skuska"
}

"""
# Registracia
@api_view(['POST'])
def register_user(request):
    # process data from POST request
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)
    print(json_data,json_data["username"],json_data["email"],json_data["password"])

    user_username = json_data["username"]
    user_email = json_data["email"]
    user_password = json_data["password"]

    # create User (django native)

    try:
        if User.objects.filter(email=user_email).exists():
            return Response({"Validation Error":"Email has been already used!"})

        if User.objects.filter(username=user_username).exists():
            return Response({"Validation Error":"Username has been already used!"})
        new_user = User.objects.create_user(
            username=user_username, email=user_email, password=user_password)
        new_user.save()
    except Exception as e:
                return Response({"Register User Response Error:":e})



    # map 1:1 (User(django native) : User_profile(our DB model) )

    
    try:
        new_user_profile = User_profile.objects.create(user=new_user)
    except Exception as e:
                return Response({"Register User Response Error:":e})


    # create firebase request for JWT
    try:
        # if there is no error then signin the user with given email and password
        
        firebase_user=authe.create_user_with_email_and_password(user_email,user_password)
    except Exception as e:

        """
        "error": {
            "code": 400,
            "message": "WEAK_PASSWORD : Password should be at least 6 characters",
            "errors": [
              {
                "message": "WEAK_PASSWORD : Password should be at least 6 characters",
                "domain": "global",
                "reason": "invalid"
              }
            ]
          }
        }
        """

        message="Invalid Credentials!"
        detail=str(json.loads(e.strerror)["error"]["message"])
        print({"FirebaseError":message})
        new_user.delete()
        print("User deleted")
        new_user_profile.delete()
        print("User_profile delted")
        return Response({"Simulated_Status":500,"FirebaseError":message,"Error":detail})
 
    print(firebase_user)
    
    # If New User is successfully added to DB & Firebase auth system, 
    # let's also bind uid (Firebase UID -> DB uuid)


    new_user_profile.uuid = firebase_user["localId"]
    new_user_profile.save()

    return Response({"Register User Response:":"User was successfully registrated."})


# config mozno presunieme inde... mozno nejaky config

"""
{
"email":"skuska@skuskasdsada.com",
"password":"skuska"
}

"""



# Prihlasenie
@api_view(['POST'])
def login_user(request):
    # process data from POST request
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)
   
    user_email = json_data["email"]
    user_password = json_data["password"]

    # request to firebase

    try:
        # if there is no error then signin the user with given email and password
        user_tokens=authe.sign_in_with_email_and_password(user_email,user_password)
    except Exception as e:
        message="Invalid Credentials!"
        print(e)
        return Response({"message":message})
    
    return Response(user_tokens)


# Odhlasenie -> na frontende -> v backende zablokovat token ???

# Vymazat ucet


########################################################################
################################## API #################################
########################################################################

@firebase_token_verification
@api_view(['GET'])
def verify_token_test_get(request):

    return Response({"Success":"This route is verified!"})


@csrf_exempt
@firebase_token_verification
@api_view(['POST'])
def verify_token_test(request):
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)

    passed_data = json_data["passed_data"]

    return Response({"Success":"This route is verified!","Your Data":passed_data})
