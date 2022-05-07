"""
common/forms.py
"""

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    # 비밀번호 입력
    password1 = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput)
    # 비밀번호 확인
    password2 = forms.CharField(label='Password confirmation', max_length=200, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'gender', 'user_email', 'birth')

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
class UserChangeForm(forms.ModelForm):
    # 사용자의 패스워드를 read 권한으로 설정하여 수정하지 못하도록 함
    user_password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_id', 'gender', 'user_email', 'birth', 'user_password')

    def clean_password(self):
        return self.initial["user_password"]
