from django.urls import path
from auth_app.views import login, logout, register, user_list, quick_login, delete, ask, filter_users

urlpatterns = [
    path('login/',          login,          name='login'),
    path('logout/',         logout,         name='logout'),
    path('quick_login',     quick_login,    name='quick_login'),
    path('ask',             ask,            name='ask'),
    path('delete',          delete,         name='delete'),
    path('filter_users',    filter_users,   name='filter_users'),
    path('register/',       register,       name='register'),
    path('user_list/',      user_list,      name='user_list'),
]
