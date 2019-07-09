"""OnlineMall URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
import main.views as main_views
import user.views as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/user',user_views.login),
    path('token/verify',user_views.verify),
    path('category/all',main_views.catagorieslist),
    path('product/by_category',main_views.getCatagory),
    path('product/recent',main_views.SPUlist),
    path('product/<str:uuid>',main_views.getSPU),
    path('store/',main_views.storeList),
    path('store/<str:id>',main_views.getStore),
    path('getAddress',main_views.getAddress),
    path('submitAddress',main_views.submitAddress),
    path('order',main_views.doOrder),
]