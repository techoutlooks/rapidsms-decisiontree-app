DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS = (
    "djtables",
    "rapidsms",
    "rapidsms.contrib.scheduler",
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    'decisiontree',
)

SITE_ID = 1

SECRET_KEY = 'super-secret',

ROOT_URLCONF = 'decisiontree.tests.urls',

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
