from django.contrib import admin
from django.urls import path,include
from .views import Bookmark,BookmarkFilter,Customer,CustomerAuth

urlpatterns = [
    

    path('create_customer',Customer.as_view()),
    path('login_customer',CustomerAuth.as_view()),
    path('create',Bookmark.as_view()),
    path('browse',BookmarkFilter.as_view())
]