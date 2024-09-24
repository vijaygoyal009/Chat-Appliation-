from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('index/', views.index, name='index'),
    path("<str:room_name>/", views.room, name="room"),
    path('logout',views.logout_user,name='Logout')
]
