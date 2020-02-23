from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)  # 送信されたemailを正規化している（大文字を全て小文字などにしている）
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError('Super user must has true')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super user must has true")
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(_("email_address"), unique=True)
    name = models.CharField(_("name"),unique=True,max_length=255,null=False,blank=False)
    first_name = models.CharField(_("first_name"), max_length=30, blank=True,null=True)
    last_name = models.CharField(_("last_name"), max_length=150, blank=True,null=True)
    description = models.CharField(_("self_intro"),max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='self_images/',null=True,blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=(
            "管理者だけ管理者サイトにログインできます"
        )
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=(
            "Activeとして扱われます"
        )
    )
    data_joined = models.DateTimeField(_('data joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # ここでusernameとして扱われるところがemail属性に置き換わった
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _('users')  # 管理者サイト用

    def get_full_name(self):

        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()  # stirpメソッドは文字列の間の空白以外を削除する

    def get_short_name(self):
        return self.first_name

    """userに対してメールを送る用のメソッド"""

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self, type="email"):
        if type == "name":
            return self.get_full_name()
        else:
            return self.email