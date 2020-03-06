from django.shortcuts import render,resolve_url,redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from .forms import *
from django.contrib.auth.views import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin


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
    queryset = Post.objects.order_by('created_at').reverse()
    context_object_name = "post_list"


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














