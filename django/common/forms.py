"""
common/forms.py
"""

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User, PostureLog


# 사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    # 비밀번호 입력
    password1 = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput)
    # 비밀번호 확인
    password2 = forms.CharField(label='Password confirmation', max_length=200, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'gender', 'email', 'birth')

    # 패스워드 검증
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 틀렸습니다.")
        return password2

    # 데이터 저장
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 사용자 수정 Form
# class UserChangeForm(forms.ModelForm):
#     # 사용자의 패스워드를 read 권한으로 설정하여 수정하지 못하도록 함
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('username', 'gender', 'email', 'birth', 'password')
#
#     def clean_password(self):
#         return self.initial["password"]

    # class Meta:
    #     model = User
    #     fields = ('username', 'gender', 'email', 'birth', 'password')
    #
    # def clean_password(self):
    #     return self.initial["password"]

from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

class CustomEmailChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class PostureLogForm(ModelForm):
    class Meta:
        model = PostureLog
        fields = '__all__'

# 비밀번호 초기화
from django.core.exceptions import ValidationError
import django.contrib.auth.forms as auth_forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class PasswordResetForm(auth_forms.PasswordResetForm):

    username = auth_forms.UsernameField(label="사용자ID")  # CharField 대신 사용

    class Meta:
        model = User
        fields = ('username', 'email',)

    # validation 절차:
    # 1. username에 대응하는 User 인스턴스의 존재성 확인
    # 2. username에 대응하는 email과 입력받은 email이 동일한지 확인

    def clean_username(self):
        data = self.cleaned_data['username']
        print(data)
        if not User.objects.filter(username=data).exists():
            raise ValidationError("해당 사용자ID가 존재하지 않습니다.")

        return data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        print(username)
        print(email)

        if username and email:
            if User.objects.get(username=username).email != email:
                raise ValidationError("사용자의 이메일 주소가 일치하지 않습니다")

    def get_users(self, email=''):
        active_users = User.objects.filter(**{
            'username__iexact': self.cleaned_data["username"],
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password()
        )

