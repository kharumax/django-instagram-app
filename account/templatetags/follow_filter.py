from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.views import get_user_model
from post.models import *

User = get_user_model()
register = template.Library()

"""
ここでは、カスタムフィルタを作成し、Ajaxを使用するためにテンプレート内で使用する関数を作成する
①ターゲットをフォロー状態に応じてボタンを変更する関数

"""

@register.filter(name="is_follow")
def is_follow(following,followed):
    if Relationship.objects.filter(follow=following,followed=followed).exists():
        return mark_safe(
            f"<button style=\"border: 0\" class=\"follow\" id=\"{followed.id}\" "
            f"type=\"submit\"><i class=\" fas fa-heart\">follow</i></button>"
        )
    else:
        return mark_safe(
            f"<button style=\"border: 0\" class=\"follow\" id=\"{followed.id}\" "
            f"type=\"submit\"><i class=\" far fa-heart\">unfollow</i></button>"
        )

