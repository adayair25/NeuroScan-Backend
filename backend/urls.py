from django.contrib import admin
from django.urls import path
from oauth.views import UserAPI, LoginAPI
from model.views import ModelYolo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserAPI.as_view(), name='users'), # Add this line
    path('login/', LoginAPI.as_view(), name='login'), # Add this line
    path('model/', ModelYolo.as_view(), name='model'), # Add this line
]
