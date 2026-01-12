from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.accounts import views as acc_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.movies.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    path('login/', acc_views.login_page, name='login'),
    path('register/', acc_views.register_page, name='register_page'),
    path('api/v1/', include('apps.reviews.urls')),
    # path('api/v1/', include('apps.movies.urls')),
    path('api/v1/auth/', include('apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)