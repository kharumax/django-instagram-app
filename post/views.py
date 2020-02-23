from django.shortcuts import render
from django.views import generic
from .models import *
from django.contrib.auth.views import get_user_model


class Top(generic.TemplateView):
    template_name = "post/top.html"

