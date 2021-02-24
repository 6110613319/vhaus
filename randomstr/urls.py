from django.urls import path 
from . import views

urlpatterns = [
	path('', views.home , name="home"),
	path('randomString/', views.randomString, name="randomString"),
    path('addRandomString',views.addRandomStr, name="addRandomString"),
	path('allRandomString', views.allRandomString, name="allRandomString"),
	path('deleteRandomString', views.deleteRandomString, name="deleteRandomString")
]