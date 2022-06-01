from django.urls import path
from .views import *

urlpatterns=[
    #path(path,function,name in html)
    path('',index),

    path('registerform',registerForm),
    path('register',register),
    path('loginform',loginForm),
    path('login',login),
    path('changepasswordform',changePassForm),
    path('changepass/<int:id>',changePass),
    path('updateprofileform',updateProfileForm),
    path('updateprofile/<int:id>',updateProfile),
    path('logout',logout),

    path('createblog',createBlog),
    path('createrecord',createRecord), 
    path('blog/<int:id>',blogDetail,name='blogdetail'), 
    path('myblog/<str:username>',myBlog,name='myblog'), 
    path('updateblog/<int:id>',updateBlog,name='updateblog'), 
    path('updateblog/updaterecord/<int:id>',updateRecord,name='updateblogrecord'), 
    path('deleteblog/<str:username>/<int:id>',deleteBlog,name='deleteblog'),

]
    
