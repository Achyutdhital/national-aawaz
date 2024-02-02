from django.urls import path, include
from . import views
from .views import *

from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static 


app_name="app"

urlpatterns = [ 
    path('', IndexListView.as_view(), name="index"),
    path('news-details/<slug:news_slug>/', NewsDetailsView.as_view(), name='newsDetails'),
    path('contact',views.contact, name='contact'),
    path('news/category',CategoryListView.as_view() , name='news_category' ),
    path('news/category/<str:main_category_slug>/', CategoryListView.as_view(), name='news_category'),
    path('news/category/<str:main_category_slug>/<str:sub_category_slug>/',CategoryListView.as_view(), name='news_category'),
    path('video',views.video, name='video'),
    path('ads',views.ads, name='ads'),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

