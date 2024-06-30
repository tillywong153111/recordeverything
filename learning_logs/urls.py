from django.urls import path
from . import views  # 确保正确导入views模块

app_name = 'learning_logs'

urlpatterns = [
    path('', views.index, name='index'),  # 确保路径与视图函数一致
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('update_todo/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
