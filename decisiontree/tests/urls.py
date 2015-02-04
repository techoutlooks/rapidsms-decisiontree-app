from django.conf.urls import include
from django.contrib import admin


admin.autodiscover()


urlpatterns = [
    (r'^admin/', include(admin.site.urls)),
    (r'^account/', include('rapidsms.urls.login_logout')),
    (r'^tree/', include('decisiontree.urls')),
]
