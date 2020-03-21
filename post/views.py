from django.shortcuts import render,resolve_url,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .models import Post,Like,Comment,Relationship
from .forms import *
from django.contrib.auth.views import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.db.models import Q

User = get_user_model()


class Top(generic.TemplateView):
    template_name = "post/top.html"


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs["pk"]


class FeedView(generic.ListView):
    model = Post
    template_name = "post/feed.html"
    queryset = Post.objects.order_by("created_at").reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if "keyword" in self.request.GET and self.request.GET["keyword"] is not None:
            keyword = self.request.GET["keyword"]
            post_list = Post.objects.all().filter(
                Q(title__icontains=keyword) |
                Q(text__icontains=keyword) |
                Q(user__name__icontains=keyword)
            ).distinct().order_by("created_at").reverse()
            context["post_list"] = post_list
        like_list = {}
        comment_list = {}
        for post in context["post_list"]:
            like_list[post.id] = Like.objects.filter(post=post)
            comment_list[post.id] = Comment.objects.filter(post=post)
        context["like_list"] = like_list
        context["comment_list"] = comment_list

        return context


class PostView(LoginRequiredMixin,generic.CreateView):
    model = Post
    template_name = "post/new.html"
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super(PostView, self).form_valid(post)

    def get_success_url(self):
        return resolve_url("post:feed")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post/detail.html"
    context_object_name = "post"


class PostDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Post
    success_url = reverse_lazy("post:feed")


class Likes(LoginRequiredMixin,View):
    model = Like
    slug_field = "post"
    slug_url_kwarg = "postId"

    def get(self,request,postId):
        user = self.request.user
        post = Post.objects.get(id=postId)
        like = Like.objects.filter(user=user,post=post)
        like_list = {}
        comment_list = {}
        # ここで既にLikeオブジェクトが存在していた場合は、削除（いいね取り消し）を行う
        #
        if like.exists():
            like.delete() # いいね取り消し
        else:
            like = Like(user=user,post=post) # いいね作成を行う
            like.save()

        like_list[post.id] = Like.objects.filter(post=post)
        comment_list[post.id] = Comment.objects.filter(post=post)
        return render(request,"post/like.html",{
            "like_list":like_list,
            "comment_list":comment_list,
            "post":post
        })


class AddComment(LoginRequiredMixin,View):
    def post(self,request,postId):
        post = Post.objects.get(id=postId)
        user = self.request.user
        like_list = {}
        comment_list = {}
        text = request.POST["comment"]

        comment = Comment(user=user,post=post,text=text)
        comment.save()

        like_list[post.id] = Like.objects.filter(post=post)
        comment_list[post.id] = Comment.objects.filter(post=post)
        return render(request, "post/like.html", {
            "like_list": like_list,
            "comment_list": comment_list,
            "post": post
        })























