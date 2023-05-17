import os
from dotenv import load_dotenv
load_dotenv()

AWS_FILE_EXPIRE = 100
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = "subtitle-extractor"
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.amazonaws.com"

STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}}
