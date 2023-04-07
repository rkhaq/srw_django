import os
from dotenv import load_dotenv

load_dotenv()

# Amazon S3 settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')  # replace with your chosen region
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
# Use Amazon S3 for storage for uploaded media files.
DEFAULT_FILE_STORAGE = 'core.cdn.backends.MediaRootS3Boto3Storage'

# Use Amazon S3 for static files storage.
STATICFILES_STORAGE = 'core.cdn.backends.StaticRootS3Boto3Storage'
