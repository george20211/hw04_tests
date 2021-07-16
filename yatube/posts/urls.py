from django.urls import path 
from django.contrib.auth import views 
from . import views 
from django.conf.urls import include 
 
#app_name = 'posts'
 
urlpatterns = [ 
    path('about/', include('about.urls', namespace='about')), 
    path('new/', views.new_post, name='new_post'), 
    path("group/<slug:slug>/", views.group_posts, name="group_posts"), 
    path("", views.index, name="index"), 
    path('signup/', include("django.contrib.auth.urls")), 
    path('<str:username>/', views.profile, name='profile'), 
    path('<str:username>/<int:post_id>/', views.post_view, name='post'), 
    path('<str:username>/<int:post_id>/edit/', views.post_edit, 
         name='post_edit'), 
    path('la/stats/', views.stats, name='stats'), 
    #path('/404', views.page_not_found, name='s404'), 
    #path('/500', views.server_error, name='s500'), 
] 