from rest_framework.response import Response
import json
import pyrebase
from .models import User_profile



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


#from .views import authe

def firebase_token_verification(view_func):
    def func_to_return(request, *args, **kwargs):
        raw_token_form_req = (request.headers['Authorization'])
        tokenId = raw_token_form_req[1:-1].split()[1]
        print(tokenId)


        # check if token is valid
        # using firebase IdToken verification func 

        # isIdTokenVerified = authe.verify(idToken_from_response)

        # https://github.com/thisbejim/Pyrebase/blob/7a652e6bd9d148da5ff6dbe7548c6d5d0dfa1109/pyrebase/pyrebase.py#L126
        decoded_token = authe.get_account_info(tokenId)
        print(decoded_token)
        #uid = decoded_token['uid']

        isIdTokenVerified = False
        if User_profile.objects.filter(uuid=decoded_token["users"][0]["localId"]).exists():
            isIdTokenVerified = True

        if isIdTokenVerified == False:
            return Response({"Failure":"Invalid token or token has expired!"})

        return view_func(request, *args, **kwargs)

    return func_to_return