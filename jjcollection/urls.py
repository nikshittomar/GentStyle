"""
URL configuration for jjcollection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from Store.views import *
from django.conf import settings
from jjcollection.views import *    

urlpatterns = [
    path('securelogin/', admin.site.urls),
    path('home/',home, name="home"),
    path('store/', include('Store.urls')),
    path('cart/', include('Carts.urls')),
    path('accounts/', include('Accounts.urls')),
    path('orders/', include('Orders.urls')),
    # put this at the end, or add a prefix like 'category/'
  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


