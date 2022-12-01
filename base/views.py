from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
import pyrebase


from django.contrib.auth.models import User
from .models import *

import json
import requests

from django.views.decorators.csrf import csrf_exempt
import uuid
import datetime



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
    #print(json_data,json_data["username"],json_data["email"],json_data["password"])

    user_username = json_data["firstName"]
    user_first_name = user_username

    user_last_name = json_data["lastName"]
    user_email = json_data["email"]
    user_password = json_data["password"]
    user_day_of_birth_raw = json_data["dateOfBirth"].split("-")
    # e.g. datetime.datetime(2020, 5, 17)
    user_day_of_birth = datetime.datetime(int(user_day_of_birth_raw[0]),int(user_day_of_birth_raw[1]),int(user_day_of_birth_raw[2]))

    # create User (django native)

    try:
        if User.objects.filter(email=user_email).exists():
            return Response({"Error":"Email has been already used!"})

        if User.objects.filter(username=user_username).exists():
            return Response({"Error":"Username has been already used!"})
        new_user = User.objects.create_user(
            username=user_username, email=user_email, password=user_password,first_name=user_first_name,last_name=user_last_name)
        new_user.save()
    except Exception as e:
                return Response({"Error:":e})



    # map 1:1 (User(django native) : User_profile(our DB model) )

    
    try:
        new_user_profile = User_profile.objects.create(user=new_user,day_of_birth=user_day_of_birth)
    except Exception as e:
                return Response({"Error:":e})


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

    # Bind chat usr and BackEnd
    # request to WS backend 
    ws_username = user_first_name +" "+ user_last_name
    ws_tukbook_usr_uuid = firebase_user["localId"]

    try:
        url = "https://pz603fr.pythonanywhere.com/create_chat_user/"

        payload = json.dumps({
        "tukbook_usr_uuid": ws_tukbook_usr_uuid,
        "username": ws_username
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    except Exception as e:
        return Response({"Error:":e})

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

# GET all users ()
#@firebase_token_verification
@api_view(['GET'])
def get_all_users(request):
    all_normal_users = User_profile.objects.all()
    array_of_all_info = [{"meno":Nuser.user.first_name,"priezvisko":Nuser.user.last_name,"uuid":Nuser.uuid} for Nuser in all_normal_users]

    return Response({"Success":"This route is verified!","Data":array_of_all_info})


# GET all posts ()
#@firebase_token_verification
@api_view(['GET'])
def get_all_posts(request):
    all_posts = User_post.objects.all()
    all_data = []
    
    for single_post in all_posts: 
        single_post_JSON = {
            "id":single_post.pk,
            "meno":single_post.profile_id.user.first_name,
            "priezvisko":single_post.profile_id.user.last_name,
            "text":Text_post.objects.get(user_post_id=single_post).text,
            "video":[x.photo_sample_url for x in Video_post.objects.filter(user_video_id=single_post)],
            "audio":[x.photo_sample_url for x in Audio_post.objects.filter(user_audio_id=single_post)],
            "image":[x.photo_sample_url for x in Photo_post.objects.filter(user_post_id=single_post)],
            "likesQty":len(Post_like.objects.filter(post_id=single_post)),
            "likers":[{"meno":liker.profile_id.user.first_name,"priezvisko":liker.profile_id.user.first_name,"email":liker.profile_id.user.first_name} for liker in Post_like.objects.filter(post_id=single_post)],
            "comments":[{"id":comment.pk,"meno":comment.profile_id.user.first_name,"priezvisko":comment.profile_id.user.last_name,"email":comment.profile_id.user.email,"createdAt":comment.created_date,"text":comment.text} for comment in Post_comment.objects.filter(post_id=single_post)],
            "createdAt":single_post.created_date
            }
        all_data.append(single_post_JSON)
 

    return Response({"Success":"This route is verified!","Data":all_data})

#@firebase_token_verification
@api_view(['GET'])
def get_user_info(request,uuid_):
    try:
        user_info = User_profile.objects.get(uuid=uuid_)
        all_data = {
            "meno":user_info.user.first_name,
            "priezvisko":user_info.user.last_name,
            "email":user_info.user.email,
            "dateOfBirth":user_info.day_of_birth
            }
        
    except Exception as e:
        return Response({"Error":str(e)})
    
    return Response({"Success":"This route is verified!","Data":all_data})



#############################################
# 
#   POST
#
#############################################


@csrf_exempt
#@firebase_token_verification
@api_view(['POST'])
def create_post(request):
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)

    user_uuid = json_data["uuid"]
    user_text = json_data["text"]

    audio_url = json_data["audio"]
    video_url = json_data["video"]
    photo_url = json_data["photo"]



    user1 = User_profile.objects.get(uuid=user_uuid)
    post1 = User_post.objects.create(profile_id=user1) 
    text1 = Text_post.objects.create(user_post_id = post1, text=user_text)

    audio1 = Audio_post.objects.create(user_audio_id = post1, photo_sample_url=audio_url)
    video1 = Video_post.objects.create(user_video_id = post1, photo_sample_url=video_url)
    photo1 = Photo_post.objects.create(user_post_id = post1, photo_sample_url=photo_url)

    return Response({"Success":"This route is verified!","Post": "created"})


@api_view(['GET'])
def delete_post(request,pk):
    try:
        post1 = User_post.objects.get(pk=pk) 
        post1.delete()
    except Exception as e:
        return Response({"Error":str(e)})
        
    return Response({"Success":"This route is verified!","Post": "deleted"})


    

@csrf_exempt
#@firebase_token_verification
@api_view(['POST'])
def create_post_comment(request):
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)

    user_uuid = json_data["uuid"]
    user_post_id = json_data["post_id"]
    comment_text = json_data["text"]

    try:
        user1 = User_profile.objects.get(uuid=user_uuid)
        post1 = User_post.objects.get(pk=user_post_id) 
        comment1 = Post_comment.objects.create(post_id=post1,profile_id=user1,text=comment_text)
    except Exception as e:
        return Response({"Error":str(e)})

    return Response({"Success":"This route is verified!","Comment": "created"})



#@firebase_token_verification
@api_view(['GET'])
def delete_post_comment(request,pk):
    try:
        post1 = Post_comment.objects.get(pk=pk) 
        post1.delete()
    except Exception as e:
        return Response({"Error":str(e)})
        
    return Response({"Success":"This route is verified!","Comment": "deleted"})



@csrf_exempt
#@firebase_token_verification
@api_view(['POST'])
def like_post(request):
    
    raw_data = request.body.decode()
    
    json_data = json.loads(raw_data)

    user_uuid = json_data["uuid"]
    user_post_id = json_data["post_id"]

    try:
        user1 = User_profile.objects.get(uuid=user_uuid)
        post1 = User_post.objects.get(pk=user_post_id) 
        like1 = Post_like.objects.create(post_id=post1,profile_id=user1)
    except Exception as e:
        return Response({"Error":str(e)})

    return Response({"Success":"This route is verified!","Comment": "created"})



#@firebase_token_verification
@api_view(['GET'])
def unlike_post(request,uuid,post_id):
    try:
        post1 = Post_comment.objects.get(pk=post_id) 
        user1 = User_profile.objects.get(uuid=uuid) 
        like1 = Post_like.objects.filter(post_id=post1).filter(profile_id=user1)
        like1.delete()
    except Exception as e:
        return Response({"Error":str(e)})
        
    return Response({"Success":"This route is verified!","Comment": "deleted"})

