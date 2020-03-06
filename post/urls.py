from django.urls import path
from . import views

app_name = "post"
urlpatterns = [
    path('',views.Top.as_view(),name="top"),
    path('posts/',views.FeedView.as_view(),name="feed"),
    path('posts/new',views.PostView.as_view(),name="post"),
    path('posts/<int:pk>/',views.PostDetailView.as_view(),name="detail"),
    path('posts/<int:pk>/delete/',views.PostDeleteView.as_view(),name="delete"),
]