
from django.contrib import admin
from django.urls import path

from .views import *



urlpatterns = [
    path('', views_email_group.mail_gorup_index, name = 'mail_group_index'),
    path('mail_group_delete', views_email_group.mail_group_delete, name = 'mail_group_delete'),
    path('mail_group_add_keyword', views_email_group.mail_group_add_keyword, name = 'mail_group_add_keyword'),
    path('mail_group_delete_keyword', views_email_group.mail_group_delete_keyword, name = 'mail_group_delete_keyword'),


    path('keyword_management', views_keyword_management.keyword_management_index, name = 'keyword_management_index'),
    path('keyword_management_edit/<int:id>', views_keyword_management.keyword_management_edit, name = 'keyword_management_edit'),
    path('keyword_management_delete', views_keyword_management.keyword_management_delete, name = 'keyword_management_delete'),


    path('exclusion_site_management', views_exclusion_site_management.exclusion_site_management_index, name = 'exclusion_site_management_index'),
    path('exclusion_site_management_delete', views_exclusion_site_management.exclusion_site_management_delete, name = 'exclusion_site_management_delete'),
]


