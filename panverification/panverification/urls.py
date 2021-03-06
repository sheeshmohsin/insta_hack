"""panverification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import panapp

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v1/', include('panapp.urls')),
    url(r'^user/$', panapp.views.user_page),
    url(r'^agent/$', panapp.views.agent_page),
    url(r'^login/$', panapp.views.login_page),
    url(r'^signup_agent/$', panapp.views.signup_agent_page),
    url(r'^signup_user/$', panapp.views.signup_user_page),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
