from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.views import get_user_model
from post.models import *

User = get_user_model()
register = template.Library()

"""
ここでは、カスタムフィルタを作成し、Ajaxを使用するためにテンプレート内で使用する関数を作成する
①ターゲットをフォロー状態に応じてボタンを変更する関数
②ターゲットをフォローしているユーザー数取得関数
③ターゲットにフォローされているユーザー数取得関数
"""


@register.filter(name="is_follow")
def is_follow(following,followed):
    try:
        user = User.objects.get(pk=following.id)
    except User.DoesNotExist:
        return mark_safe("")
    else:
        if following != followed:
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
        else:
            return mark_safe(
                "self"
            )


@register.filter(name="following_count")
def following_count(user):
    following_cnt = Relationship.objects.filter(follow=user).count()
    # ここでユーザーがフォローしているユーザー数を取得する
    return mark_safe(
        f"<div class=\"following_cnt\">following : {following_cnt}</div>"
    )


@register.filter(name="followed_count")
def followed_count(user):
    followed_cnt = Relationship.objects.filter(followed=user).count()
    # ここでユーザーをフォローしているユーザー数を取得する
    return mark_safe(
        f"<div class=\"followed_cnt\">followers : {followed_cnt}</div>"
    )

