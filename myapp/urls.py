from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('get/', views.get, name='get'),
    path('create/', views.create, name='create'),
    path('edit/<str:id>/', views.edit, name='edit'),  # URL pattern for edit user
    path('delete/<str:id>/', views.delete, name='delete'),
]
