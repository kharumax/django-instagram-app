from django.shortcuts import render,redirect,resolve_url
from .models import *
from django.conf import settings
from django.views import generic
from django.contrib.auth.views import LoginView,LogoutView
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404,HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin

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
        user.is_active = False #仮登録なのでまだ有効化しない
        user.save() #DBに一旦登録する

        current_site = get_current_site(self.request) #現在のページを取得
        print("This is self.request : {}".format(self.request))
        domain = current_site.domain

        context = {
            "protocol" : self.request.scheme,
            "domain" : domain,
            "token" : dumps(user.pk),
            "user" : user
        }

        subject = render_to_string("account/mail_template/signup/subject.txt",context)
        message = render_to_string("account/mail_template/signup/message.txt",context)

        user.email_user(subject,message)

        return redirect("account:signup_done")


class SignupDone(generic.TemplateView):
    """仮登録完了通知"""
    template_name = "account/signup_done.html"


class SignupComplete(generic.TemplateView):
    template_name = "account/signup_complete.html"
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        token = self.kwargs.get("token") #URLから<token>を取得する
        try:
            user_pk = loads(token,max_age=self.timeout_seconds)

        #tokenが期限切れになっている
        except SignatureExpired:
            return HttpResponseBadRequest

        #tokenが違う
        except BadSignature:
            return HttpResponseBadRequest

        #tokenに問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request,**kwargs)
        return HttpResponseBadRequest




















