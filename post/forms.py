from django import forms
from .models import *

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title","text","image","hash")

    def __init__(self,*args,**kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

            
