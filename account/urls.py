from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('',views.Test.as_view(),name="test"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('signup/',views.Signup.as_view(),name="signup"),
    path('signup/done/',views.SignupDone.as_view(),name="signup_done"),
    path('signup/complete/<token>/',views.SignupComplete.as_view(),name="signup_complete"),

]