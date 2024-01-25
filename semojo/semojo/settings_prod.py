from .settings import *

DEBUG = False

# We are behing a reverse proxy, so we can allow all hosts
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://semojo.vmois.dev']
