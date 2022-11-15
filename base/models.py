from enum import unique
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
# available model fields:
# https://docs.djangoproject.com/en/4.1/ref/models/fields/


# Native django User model -> set email as unique field:
# https://stackoverflow.com/a/64075027
User._meta.get_field('email')._unique = True


class User_profile(models.Model):
    # bind Django User model with our custom User_profile
    # default django (obsahuje: username,first/last_name,email,password, groups, user_permisstions...)
    # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#datetimefield
    # DateTimeField -> represent Python datetime.datetime
    # e.g. datetime.datetime(2020, 5, 17)
    day_of_birth = models.DateTimeField(blank=True, null=True)
    country = models.TextField(max_length=30,blank=True)
    phone_number =  models.TextField(max_length=16,blank=True)
    # auto_now_add=True -> automatically asign date when created
    registration_date = models.DateField(auto_now_add=True)
    friend = models.ManyToManyField("User_profile", blank=True)
    # ADDED P.Z.:
    # url of img 
    profile_pic_url = models.URLField(max_length=400, blank=True)
    # about user text-field
    about = models.TextField(null=True, blank=False)
    # UUID due to match w firebase JWT DB
    uuid = models.TextField(max_length=50,blank=True)

    # gender Muž/Žena/Iné
    GENDER = [
    ('M', 'Muž'),
    ('F', 'Žena'),
    ('O', 'Iné')   
    ]

    genders = models.CharField(
        max_length=4,
        choices=GENDER,
        null = True,
        blank = True,
        default = "O"
    )

    def __str__(self):
        return "User_profile ID: %s | Email: %s" % (self.pk,self.user.email) 





#################  POST  #################

class User_post(models.Model):
    # 1:M, if user is deleted, posts are also deleted (CASCADE)
    # 1 User can have multiple posts
    profile_id = models.ForeignKey(User_profile,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)  
    shared_counter = models.IntegerField(default=0) 

    def __str__(self):
        return "User_post ID: %s | User_post text : %s..." % (self.pk,self.text[::20]) 



class Post_like(models.Model):
    post_id = models.ForeignKey(User_post,on_delete=models.CASCADE)
    profile_id = models.ForeignKey(User_profile,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True) 
    #state = models.BooleanField(default=True) True/False ???
    def __str__(self):
        return "Post_like ID: %s | User_profile ID : %s" % (self.pk,self.profile_id) 

class Post_comment(models.Model):
    post_id = models.ForeignKey(User_post,on_delete=models.CASCADE)
    profile_id = models.ForeignKey(User_profile,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    text = models.TextField(null=True, blank=False)

    def __str__(self):
        return "Post_comment ID: %s | User_profile ID : %s" % (self.pk,self.profile_id) 


class Text_post(models.Model):
    user_post_id = models.OneToOneField(User_post,on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=False)
    
    def __str__(self):
        return "Text_post ID: %s | user_post ID : %s" % (self.pk,self.user_post_id) 

class Photo_post(models.Model):
    user_post_id = models.ForeignKey(User_post,on_delete=models.CASCADE)
    photo_sample_url = models.URLField(max_length=400, blank=True)

    def __str__(self):
        return "Photo_post ID: %s | user_post ID : %s" % (self.pk,self.user_post_id) 

class Audio_post(models.Model):
    user_audio_id = models.ForeignKey(User_post,on_delete=models.CASCADE)
    photo_sample_url = models.URLField(max_length=400, blank=True)

    def __str__(self):
        return "Audio_post ID: %s | user_post ID : %s" % (self.pk,self.user_post_id) 

class Video_post(models.Model):
    user_video_id = models.ForeignKey(User_post,on_delete=models.CASCADE)
    photo_sample_url = models.URLField(max_length=400, blank=True)

    def __str__(self):
        return "Video_post ID: %s | user_post ID : %s" % (self.pk,self.user_post_id) 


#################  Requests  #################


class Friendship_request(models.Model):
    sender_id = models.OneToOneField(User_profile,on_delete=models.CASCADE, related_name="friendship_sender_id")
    receiver_id = models.OneToOneField(User_profile,on_delete=models.CASCADE, related_name="friendship_receiver_id")
    request_state = models.BooleanField(default=True)


    def __str__(self):
        return "Friendship_request ID: %s | sender_id ID : %s | receiver_id ID : %s" % (self.pk,self.sender_id,self.receiver_id) 

class Follow_request(models.Model):
    sender_id = models.OneToOneField(User_profile,on_delete=models.CASCADE, related_name="follow_sender_id")
    receiver_id = models.OneToOneField(User_profile,on_delete=models.CASCADE, related_name="follow_receiver_id")
    request_state = models.BooleanField(default=True)

    def __str__(self):
        return "Follow_request ID: %s | sender_id ID : %s | receiver_id ID : %s" % (self.pk,self.sender_id,self.receiver_id) 

"""
class Messages(models.Model):
    pass

"""

