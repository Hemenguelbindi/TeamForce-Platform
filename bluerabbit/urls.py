from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls'))
]
