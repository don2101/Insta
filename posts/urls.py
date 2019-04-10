from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
    path('<int:post_num>/delete/', views.delete, name="delete"),
    path('<int:post_num>/update/', views.update, name="update"),
]