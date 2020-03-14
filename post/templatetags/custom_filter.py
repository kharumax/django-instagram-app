from django import template
from django.utils.safestring import mark_safe
from ..models import Like,Comment,Post
register = template.Library() # カスタムフィルタとして扱うための宣言

"""ここでは、カスタムフィルタを作成するAjaxを使用するために、テンプレート内で複雑な処理を行えるようにするため
   主な、処理は3つ
   ①いいねしたユーザーの情報を返す関数
   ②リクエストユーザーが「いいね」しているかどうかでいいね作成・削除の処理をわける関数
   ③特定のコメントに関するデータを返す関数
   ④いいね数を返す関数
   ⑤コメント数を返す関数
"""


@register.filter(name="get_likes")
def get_likes(like_list,key):
    # like_listはViewから渡されるコンテキスト変数
    # keyはPostモデルのIDを受け取る key = post.id
    text = ""
    if key in like_list:
        text = ""
        for like in like_list[key]: #like = Likeオブジェクト
            text += f"{like.user.name},"
            text += "がいいねしました"
        return text

# いいねしているなら「いいね削除」、してないなら「いいね作成」
@register.filter(name="is_like")
def is_like(post,user):
    if Like.objects.filter(user=user,post=post).exists():
        return mark_safe(
            f"<button style=\"border: 0\" class=\"like\" id=\"{post.id}\" "
            f"type=\"submit\"><i class=\" fas fa-heart\" style=\" background:red \"></i></button>"
        )
    else:
        return mark_safe(
            f"<button style=\"border: 0\" class=\"like\" id=\"{post.id}\" "
            f"type=\"submit\"><i class=\" far fa-heart\"></i></button>"
        )


@register.filter(name="like_count")
def like_count(post):
    like_cnt = Like.objects.filter(post=post).count() # ここでターゲットの投稿のいいね数を取得する
    return mark_safe(
        f"<div>{like_cnt}</div>"
    )


@register.filter(name="get_comment_list")
def get_comment_list(comment_list,key):
    text = ""
    if key in comment_list:
        for comment in comment_list[key]:
            text += f"{comment.user.name}: {comment.text}<br>"
    return mark_safe(text)


@register.filter(name="comment_count")
def comment_count(post):
    comment_cnt = Comment.objects.filter(post=post).count() # ここでターゲットの投稿のコメント数を取得する
    return mark_safe(
        f"<div>{comment_cnt}</div>"
    )





























