import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# ==========================================
# 1. مسارات المشروع الأساسية
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 2. كشف البيئة تلقائياً (السر هنا!)
# ==========================================
# إذا وُجد ملف .env → نحن على الوكل المحلي (MySQL)
# إذا لم يُوجد → نحن على الاستضافة (SQLite)
IS_LOCAL = os.path.exists(BASE_DIR / '.env')

if IS_LOCAL:
    load_dotenv(BASE_DIR / '.env')


# ==========================================
# 3. إعدادات الأمان الأساسية (السرية)
# ==========================================
# المفتاح السري: يُقرأ من .env محلياً، أو يُستخدم بديل آمن على الاستضافة
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-)hu-ahh&uj3$f2+w$f1t08bv!z)9vs3#)5u8h@)sw)rfosizi0') if IS_LOCAL else 'prod-secret-key-change-me-later-in-env'

# وضع التطوير: تلقائي حسب البيئة
DEBUG = IS_LOCAL  

# المضيفون المسموح لهم: تلقائي حسب البيئة
if IS_LOCAL:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.108']
else:
    ALLOWED_HOSTS = ['wcom.pythonanywhere.com']


# ==========================================
# 4. التطبيقات المثبتة
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',  
    'invoice.apps.InvoiceConfig',
]

# ==========================================
# 5. البرمجيات الوسيطة (Middleware)
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'balanceIQ.urls'

# ==========================================
# 6. إعدادات القوالب (Templates)
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.site_settings',
                'invoice.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'balanceIQ.wsgi.application'


# ==========================================
# 7. قاعدة البيانات (تلقائي حسب البيئة)
# ==========================================
if IS_LOCAL:
    # ===== وضع الوكل المحلي (MySQL) =====
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'accounting_db',
            'USER': 'root',
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        }
    }
else:
    # ===== وضع الاستضافة (SQLite مؤقت) =====
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==========================================
# 8. التحقق من صحة كلمات المرور
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 9}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================
# 9. اللغة والوقت
# ==========================================
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Amman'
USE_I18N = True
USE_TZ = True


# ==========================================
# 10. الملفات الثابتة (Static) والملفات المرفوعة (Media)
# ==========================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# 11. إعدادات المصادقة وتسجيل الدخول
# ==========================================
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'accounts:login'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False  
SESSION_COOKIE_AGE = 1209600  
PASSWORD_RESET_TIMEOUT = 86400  

# رابط الموقع: تلقائي حسب البيئة
SITE_URL = 'http://localhost:8000' if IS_LOCAL else 'https://ahmadkh511.pythonanywhere.com'


# ==========================================
# 12. إعدادات الأمان (تلقائي حسب البيئة)
# ==========================================
if IS_LOCAL:
    CSRF_COOKIE_SECURE = False  
    SESSION_COOKIE_SECURE = False  
else:
    CSRF_COOKIE_SECURE = True  
    SESSION_COOKIE_SECURE = True  


# ==========================================
# 13. نظام تسجيل الأحداث (Logging)
# ==========================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {asctime} {message}', 'style': '{'},
        'detailed': {'format': '{asctime} | {levelname:8s} | {name:20s} | {message}', 'style': '{', 'datefmt': '%Y-%m-%d %H:%M:%S'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple', 'level': 'INFO'},
        'file_debug': {'class': 'logging.FileHandler', 'filename': os.path.join(BASE_DIR, 'logs/debug.log'), 'formatter': 'detailed', 'level': 'DEBUG'},
        'file_errors': {'class': 'logging.FileHandler', 'filename': os.path.join(BASE_DIR, 'logs/errors.log'), 'formatter': 'verbose', 'level': 'ERROR'},
        'file_info': {'class': 'logging.FileHandler', 'filename': os.path.join(BASE_DIR, 'logs/info.log'), 'formatter': 'detailed', 'level': 'INFO'},
    },
    'loggers': {
        'django': {'handlers': ['console', 'file_info'], 'level': 'INFO', 'propagate': True},
        'django.request': {'handlers': ['file_info', 'file_errors'], 'level': 'DEBUG', 'propagate': False},
        'invoice': {'handlers': ['console', 'file_debug', 'file_errors'], 'level': 'DEBUG', 'propagate': False},
        'invoice.models': {'handlers': ['file_debug'], 'level': 'DEBUG', 'propagate': False},
        'invoice.views': {'handlers': ['console', 'file_debug'], 'level': 'DEBUG', 'propagate': False},
        'invoice.forms': {'handlers': ['file_debug'], 'level': 'DEBUG', 'propagate': False},
    },
}