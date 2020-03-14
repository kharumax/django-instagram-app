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
    path('<int:pk>/',views.ShowView.as_view(),name="show"),
    path('<int:pk>/feeds/',views.UserFeedView.as_view(),name="user_feeds"),
    path('<int:pk>/update/',views.InfoUpdateView.as_view(),name="update"),
    path('list/',views.UserListView.as_view(),name="list"),
    path('<int:userId>/follow/',views.FollowView.as_view(),name="follow"),
    path('<int:pk>/followings/',views.FollowingView.as_view(),name="followings"),
    path('<int:pk>/followers/',views.FollowersView.as_view(),name="followers"),
]