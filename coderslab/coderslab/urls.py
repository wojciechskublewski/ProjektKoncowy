"""coderslab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from brc_db.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name='base_view'),
    path('add_CIM/', OpenCIMView.as_view(), name='add_cim'),
    path('add_PM/', PMCreateView.as_view(), name='add_pm'),
    path('add_SR/', SpecialRestrictionCreateView.as_view(), name='add_special_restrictions'),
    path('update_CIM/<pk>/', UpdateCIMView.as_view(), name='update_cim'),
    path('pre_maker_review/', PREMakerView.as_view(), name='create_pre_maker'),
    path('pre_review_list/', PREREviewListView.as_view(), name='create_pre_maker'),


]
