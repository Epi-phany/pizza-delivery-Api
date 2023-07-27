from django.urls import path
from .views import UserCreateView,UserView,LogInView

urlpatterns = [
    #path('',HelloAuthView.as_view(),name='hello auth'),
    path('',UserView.as_view(),name='User_list'),
    path('signup/',UserCreateView.as_view(),name='signUp'),
]