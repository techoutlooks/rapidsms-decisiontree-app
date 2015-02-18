from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = [
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^account/',
        include('rapidsms.urls.login_logout')),
    url(r'^(?P<group_slug>[\w-]+)/(?P<tenant_slug>[\w-]+)/tree/',
        include('decisiontree.urls')),
    url(r'^',
        include('multitenancy.urls')),
]
