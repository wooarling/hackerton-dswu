from pathlib import Path
import os

# -----------------------------
# 기본 경로 설정
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# 보안 및 디버그
# -----------------------------
SECRET_KEY = 'django-insecure-#q43mc^!2o4jd4ydz%gdqkejdj*=ag7i5j4@mnofmx0lniud@a'
DEBUG = True
ALLOWED_HOSTS = ['*']

# -----------------------------
# 커스텀 유저 모델
# -----------------------------
AUTH_USER_MODEL = 'accounts.User'

# -----------------------------
# 설치된 앱
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Local apps
    'it_test',
    'accounts',
    'board',
]

# -----------------------------
# REST Framework 설정
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# -----------------------------
# 미들웨어
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL 설정
# -----------------------------
ROOT_URLCONF = 'hackerton_dswu.urls'

# -----------------------------
# 템플릿 설정
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'hackerton_dswu' / 'templates'],  # 프로젝트 템플릿 폴더
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------------
# WSGI 설정
# -----------------------------
WSGI_APPLICATION = 'hackerton_dswu.wsgi.application'

# -----------------------------
# 데이터베이스
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------
# 비밀번호 검증
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# 지역화
# -----------------------------
LANGUAGE_CODE = 'en-us'

# 시간대 설정을 서울로 변경
TIME_ZONE = 'Asia/Seoul'  # 서울 시간으로 설정
USE_I18N = True
USE_TZ = True  # 시간대 사용을 활성화

# -----------------------------
# 정적 파일(CSS, JS)
# -----------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "hackerton_dswu", "static"),
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # 배포 시 사용 (optional)

# -----------------------------
# 미디어 파일 (업로드 파일 저장)
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# 기본 자동 필드
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
