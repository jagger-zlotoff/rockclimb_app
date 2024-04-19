from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import register
from . import views
from .views import active_rockvideos, update_rockVideo, delete_rockVideo_confirm, home



urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('routes/', views.index, name='index'),
path('', views.home, name='home'),
path('login/', auth_views.LoginView.as_view(template_name='rockclimb_app/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
path('register/', views.register, name='register'),
path('active-rockVideos/', active_rockvideos, name='active_rockvideos'),
path('rockVideo/<int:pk>/', views.rockVideo_detail, name='rockVideo-detail'), 
path('rockVideo/update/<int:pk>/', update_rockVideo, name='rockVideo-update'),   
path('rockVideo/delete/<int:pk>/', delete_rockVideo_confirm, name='rockVideo-delete-confirm'),
path('rockVideo/add/', views.add_rockVideo, name='rockVideo-add'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)