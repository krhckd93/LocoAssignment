from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('', views.index, name='index'),
    path('create', models.create_comment, name='comment_create'),
    path('get', models.get_comments, name='get_comments'),
    path('delete', models.delete_comment, name='delete_user'),
    path('getUserComments', models.get_user_comments, name='get_user_comments')
]