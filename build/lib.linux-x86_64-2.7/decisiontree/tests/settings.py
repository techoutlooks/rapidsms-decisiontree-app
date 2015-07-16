TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rapidsms",
    "multitenancy",

    "decisiontree",
    "decisiontree.multitenancy",
]

INSTALLED_BACKENDS = {
    'message_tester': {
        'ENGINE': 'rapidsms.backends.database.DatabaseBackend',
    },
}

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'multitenancy.middleware.MultitenancyMiddleware',
]

ROOT_URLCONF = 'decisiontree.tests.urls'

SECRET_KEY = 'super-secret'

SITE_ID = 1

STATIC_URL = '/static/'
