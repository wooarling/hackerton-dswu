from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

#  UserManager 정의
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("아이디는 필수입니다.")
        email = self.normalize_email(extra_fields.get('email'))
        extra_fields['email'] = email
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError("비밀번호는 필수입니다.")
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

#  User 모델 정의
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 그룹/권한 필드에 related_name 지정
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()  

    def __str__(self):
        return self.username