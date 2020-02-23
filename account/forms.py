from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,UserChangeForm,AuthenticationForm,
    PasswordResetForm,PasswordChangeForm,SetPasswordForm
)
User = get_user_model()


class LoginForm(AuthenticationForm):

    def __init__(self,*args,**kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","name",)

    # フォームのデザインを制御する
    def __init__(self,*args,**kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        """仮登録していたが、本登録をしていないユーザーのメアドを削除している"""
        """活用例：あるメアドxで登録していたが、期限切れになる。そのあとに登録するも期間がすぎており、登録できないので再度仮登録させる"""
        email = self.cleaned_data["email"] #ここでEmailを取得する
        User.objects.filter(email=email,is_active=False).delete()
        return email
















