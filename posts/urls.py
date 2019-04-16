from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
    path('<int:post_num>/delete/', views.delete, name="delete"),
    path('<int:post_num>/update/', views.update, name="update"),
    path('<int:post_num>/like/', views.like, name="like"),
    path('<int:post_num>/comment/create/', views.create_comment, name="create_comment"),
    path('<int:post_num>/comment/<int:comment_num>/delete/', views.delete_comment, name="delete_comment"),
]