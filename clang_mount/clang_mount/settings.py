
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-92$ow+f^b^eu90+r_8q3mab06&6@&0e@7yfb#x1q(^^_jeg_a8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'admin_side.apps.AdminSideConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_side.apps.UserSideConfig',
    'customer_details.apps.CustomerDetailsConfig',
    'pro_category.apps.ProCategoryConfig',
    'product.apps.ProductConfig',
    'account.apps.AccountConfig',
    'cart.apps.CartConfig',
    'shop.apps.ShopConfig',
    'order.apps.OrderConfig',
    'coupon.apps.CouponConfig',
    'wallet.apps.WalletConfig',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'clang_mount.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.car_fuc',
                'cart.context_processors.wishlist_func',
                'cart.context_processors.wallet_func',
                'social_django.context_processors.backends',
            ],
        },
    },
]

WSGI_APPLICATION = 'clang_mount.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clang_mount',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR,'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'admin_side.User'  # Point to your custom user model

#email_host
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "clangmount@gmail.com"
EMAIL_HOST_PASSWORD = "ekhukgmmrpvhaken"
EMAIL_USE_TLS = True




#RAZORPAY
KEY = 'rzp_test_DadhvgCTL7p70u'
SECRET_KEY = 'o7iNqzNVyDMRokNUTNazpAVS'


#social
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
LOGIN_URL = 'user_app:user_login'
LOGIN_REDIRECT_URL = 'shop_app:index'
LOGOUT_URL = 'user_app:user_logout'
LOGOUT_REDIRECT_URL = 'user_app:user_login'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "52100197078-hltg3m213u5j8qk2l7sb424573nrjfj1.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

# image cropping
