from django.urls import path,include
from . import views

from farmers.views import post_detail
app_name = 'farmers'

urlpatterns = [
    #Home page
    path('', views.index,name='index'),
    path ('crops/', views.crops, name='crops'),
    path ('wakulima/', views.wakulima, name='wakulima'),
    path ('news/', views.news, name='news'),
    path ('thatpdf/', views.thatpdf, name='thatpdf'),
    
    path ('contact/', views.contact, name='contact'),
    path('crops/<int:crop_id>/', views.crop, name='crop'),
    # page for adding a new crop
    path('new_crop/', views.new_crop, name='new_crop'),
    path('new_entry/<int:crop_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path ('<slug:slug>/', views.post_detail, name='post_detail'),
]