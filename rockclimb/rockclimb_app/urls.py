from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import active_rockvideos, update_rockVideo, delete_rockVideo_confirm



urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('', views.index, name='index'),
path('login/', auth_views.LoginView.as_view(), name='login'),
path('active-rockVideos/', active_rockvideos, name='active_rockvideos'),
path('rockVideo/<int:pk>/', views.rockVideo_detail, name='rockVideo-detail'), 
path('rockVideo/update/<int:pk>/', update_rockVideo, name='rockVideo-update'),   
path('rockVideo/delete/<int:pk>/', delete_rockVideo_confirm, name='rockVideo-delete-confirm'),
path('rockVideo/add/', views.add_rockVideo, name='rockVideo-add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)