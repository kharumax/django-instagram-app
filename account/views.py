from django.shortcuts import render, redirect, resolve_url
from .models import *
from django.conf import settings
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin,LoginRequiredMixin
from post.models import *

User = get_user_model()


class Test(generic.TemplateView):
    template_name = "account/test.html"

    def get_context_data(self, **kwargs):
        test = "This is test"
        context = super(Test, self).get_context_data(**kwargs)
        context["test"] = test
        return context


class Login(LoginView):
    template_name = "account/login.html"
    form_class = LoginForm
    success_url = "post:top"


class Logout(LogoutView):
    template_name = "post/top.html"


class Signup(generic.CreateView):
    """仮登録を行うView"""
    template_name = "account/signup.html"
    form_class = SignUpForm
    success_url = "post:top"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # 仮登録なのでまだ有効化しない
        user.name = "@"+user.name
        user.save()  # DBに一旦登録する

        current_site = get_current_site(self.request)  # 現在のページを取得
        print("This is self.request : {}".format(self.request))
        domain = current_site.domain

        context = {
            "protocol": self.request.scheme,
            "domain": domain,
            "token": dumps(user.pk),
            "user": user
        }

        subject = render_to_string("account/mail_template/signup/subject.txt", context)
        message = render_to_string("account/mail_template/signup/message.txt", context)

        user.email_user(subject, message)

        return redirect("account:signup_done")


class SignupDone(generic.TemplateView):
    """仮登録完了通知"""
    template_name = "account/signup_done.html"


class SignupComplete(generic.TemplateView):
    template_name = "account/signup_complete.html"
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, **kwargs):
        token = self.kwargs.get("token")  # URLから<token>を取得する
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # tokenが期限切れになっている
        except SignatureExpired:
            return HttpResponseBadRequest

        # tokenが違う
        except BadSignature:
            return HttpResponseBadRequest

        # tokenに問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest


class ShowView(generic.DetailView):
    """ユーザー詳細ページ"""
    model = User
    template_name = "account/show.html"
    context_object_name = "user_info"


class OnlyYouMixin(UserPassesTestMixin):
    """Trueなら403ページに遷移させる、Falseならログインページに移動"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs["pk"]


class InfoUpdateView(OnlyYouMixin,generic.UpdateView):
    model = User
    template_name = "account/edit.html"
    form_class = UpdateForm

    def get_success_url(self):
        return resolve_url("account:show",pk=self.kwargs["pk"])


class UserFeedView(generic.TemplateView):
    template_name = "account/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_pk = self.kwargs["pk"]
        page_user = User.objects.get(pk=user_pk)
        feeds = Post.objects.filter(user=page_user)
        context["page_user"] = page_user
        context["feeds"] = feeds
        return context


class UserListView(generic.ListView):
    model = User
    template_name = "account/list.html"
    context_object_name = "user_list"


class FollowView(LoginRequiredMixin,generic.View):
    model = Relationship
    slug_field = "user"
    slug_kwarg = "userId"

    def get(self,request,userId):
        following = self.request.user # フォローする側が現在のユーザー
        followed = User.objects.get(id=userId)
        follow = Relationship.objects.filter(follow=following,followed=followed)

        if follow.exists(): # 既にフォローしている場合は削除する
            follow.delete()
        else:
            follow = Relationship(follow=following,followed=followed)
            follow.save()

        # ここで現在参照しているユーザーがフォローとフォロワーの集合をビューに返す
        followers_ids = Relationship.objects.filter(follow=followed) # フォロー集合
        followers = User.objects.filter(id__in=followers_ids)
        followed_ids = Relationship.objects.filter(followed=followed) # フォロワー集合
        followeds = User.objects.filter(id__in=followed_ids)

        return render(request,"account/follow.html",{
            "following":following,
            "followed" :followed,
            "follow":follow,
            "followers":followers,
            "followeds":followeds
        })


class FollowingView(generic.ListView):
    model = User
    template_name = "account/following.html"
    context_object_name = "following_list"

    def get_queryset(self):
        user_pk = self.kwargs["pk"]
        user = User.objects.get(pk=user_pk)
        following_ids = Relationship.objects.filter(follow=user).values_list("followed",flat=True) # ここでフォロー元がユーザーのリレー
        following = User.objects.filter(id__in=following_ids)
        return following


class FollowersView(generic.ListView):
    model = User
    template_name = "account/followers.html"
    context_object_name = "followers_list"

    def get_queryset(self):
        user_pk = self.kwargs["pk"]
        user = User.objects.get(pk=user_pk)
        followers_ids = Relationship.objects.filter(followed=user).values_list("follow", flat=True)  # ここでフォロー元がユーザーのリレー
        followers = User.objects.filter(id__in=followers_ids)
        return followers








