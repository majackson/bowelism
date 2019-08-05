import os


AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')

# S3 Config (staticfiles)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = 'bowelism-static'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_IS_GZIPPED = True
AWS_S3_REGION_NAME = AWS_DEFAULT_REGION
AWS_S3_USE_SSL = True

# This controls how the `static` template tag from `staticfiles` gets expanded.
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)


# SES Config (emails)
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = AWS_DEFAULT_REGION
AWS_SES_REGION_ENDPOINT = 'email.{}.amazonaws.com'.format(AWS_SES_REGION_NAME)


# This is used by the `static` template tag from `static`,
# Or if anything else refers directly to STATIC_URL
STATIC_URL = "https://{}/".format(AWS_S3_CUSTOM_DOMAIN)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': int(os.environ.get('DATABASE_PORT', 5432)),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
    }
}
