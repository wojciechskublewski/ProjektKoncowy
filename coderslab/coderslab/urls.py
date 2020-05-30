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
from django.contrib.admin import site
from django.urls import path
from brc_db.views import *

urlpatterns = [

    path('admin/', site.urls),
    path('login/', LoginView.as_view(), name='login_view'),
    path('', BaseView.as_view(), name='base_view'),
    path('add_CIM/', OpenCIMView.as_view(), name='add_cim'),
    path('add_PM/', PMCreateView.as_view(), name='add_pm'),
    path('add_SR/', SpecialRestrictionCreateView.as_view(), name='add_special_restrictions'),
    path('update_CIM/<pk>/', UpdateCIMView.as_view(), name='update_cim'),
    path('update_closing_CIM/<pk>/', ClosedAccountUpdateView.as_view(), name='update_closing_cim'),
    path('update_funded_CIM/<pk>/', FundedAccountUpdateView.as_view(), name='update_funded_cim'),
    path('pre_maker_review/', PREMakerView.as_view(), name='create_pre_maker'),
    path('pre_review_list/', PREREviewListView.as_view(), name='create_pre_maker'),
    path('add_lv/', LVCreateView.as_view(), name='create_lv'),
    path('add_region/', RegionCreatView.as_view(), name='create_region'),
    path('add_change/', ChangesCreateView.as_view(), name='create_change'),
    path('changes_list/', ChangesReviewMakerListView.as_view(), name='list_change_maker'),
    path('post_list/', POSTReviewNotDoneListView.as_view(), name='list_post_maker'),
    path('pre_maker_checklist/<pk>/', MakerPreChecklistView.as_view(), name='pre_maker_checklist'),
    path('pre_checker_checklist/<pk>/', PreCheckerReviewView.as_view(), name='pre_checker_checklist'),
    path('post_maker_checklist/<pk>/', MakerPostChecklistView.as_view(), name='post_maker_checklist'),
    path('post_checker_checklist/<pk>/', PostCheckerReviewView.as_view(), name='post_checker_checklist'),
    path('changes_maker_review/<pk>/', ChangesReviewMakerView.as_view(), name='change_maker_checklist'),
    path('changes_checker_review/<pk>/', ChangesCheckerReviewView.as_view(), name='change_checker_checklist'),
    path('cim_details/<cim>/', CIMDetailsView.as_view(), name='cim_details'),
    path('pars_date_search/', PARDateQuery.as_view(), name='par_date_search'),
    path('search/', CIMSearchView.as_view(), name='cim_search'),
    path('pars_date_search_to_excel/<start_date>/<end_date>/', PARDateSearchToExcel.as_view(), name='par_date_search_to_excel'),


]
