from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "post"
urlpatterns = [
    path('',views.Top.as_view(),name="top"),
    path('posts/',views.FeedView.as_view(),name="feed"),
    path('posts/new',views.PostView.as_view(),name="post"),
    path('posts/<int:pk>/',views.PostDetailView.as_view(),name="detail"),
    path('posts/<int:pk>/delete/',views.PostDeleteView.as_view(),name="delete"),
    path('posts/<postId>/like/',login_required(views.Likes.as_view()),name="like"),
    path('posts/<postId>/comment/',login_required(views.AddComment.as_view()),name="comment"),

]

# likeとcommentでは、Viewを呼び出す前にログイン有無を確認
# ログインしていないとログインURLに飛ばす



