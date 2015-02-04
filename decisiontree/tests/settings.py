DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS = [
    "rapidsms",

    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.messages",

    'decisiontree',
]

INSTALLED_BACKENDS = {
    'message_tester': {
        'ENGINE': 'rapidsms.backends.database.DatabaseBackend',
    },
}

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'decisiontree.tests.urls',

SECRET_KEY = 'super-secret',

SITE_ID = 1

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
