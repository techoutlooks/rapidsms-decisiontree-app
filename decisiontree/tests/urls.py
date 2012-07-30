from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^account/', include('rapidsms.urls.login_logout')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    (r'^tree/', include('decisiontree.urls')),
)
