from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=255,blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images/")
    hash = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    target = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.IntegerField()

    def __str__(self):
        return self.target


class Comment(models.Model):
    target = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Relationship(models.Model):
    # フォローしているユーザー（例：あるユーザーAが別のユーザーBをフォローするとき、B = A.follow)
    follow = models.ForeignKey(User,related_name="follow",
                               on_delete=models.CASCADE)
    followed = models.ForeignKey(User,related_name="followed",on_delete=models.CASCADE)

