from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, user_id, gender, user_email, birth, user_password=None):
        if not user_email:
            raise ValueError('must have user email')
        if not user_id:
            raise ValueError('must have user user_id')
        if not gender:
            raise ValueError('must have user gender')
        if not birth:
            raise ValueError('must have user birth')

        user = self.model(
            user_email = self.normalize_email(user_email),
            user_id = user_id,
            gender = gender,
            birth = birth
        )
        user.set_password(user_password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, user_id, gender, user_email, birth, user_password=None):
        user = self.model(
            user_id,
            user_email = self.normalize_email(user_email),
            user_password = user_password,
            gender = gender,
            birth = birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    user_id = models.CharField(default='', max_length=100, null=False, blank=False)
    user_email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    gender = models.CharField(default='', max_length=100, null=False, blank=False)
    birth = models.CharField(default='', max_length=100, null=False, blank=False)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'user_id'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email', 'user_id']

    def __str__(self):
        return self.user_id

    # True를 반환하여 권한이 있는 것을 알림
    # Object 반환 시 해당 Object로 사용 권한을 확인하는 절차가 필요함
    def has_perm(self, perm, obj=None):
        return True

    # True를 반환하여 주어진 App의 Model에 접근 가능하도록 함
    def has_module_perms(self, app_label):
        return True

    # True 반환 시 Django의 관리자 화면에 로그인 가능
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'