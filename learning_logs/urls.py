"""定义learning_logs的URL模式"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),

    # 显示所有主题的页面
    path('topics/', views.topics, name='topics'),

    # 显示特定主题的页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    
    #用于添加新主题的网页
    path('new_topic/',views.new_topic,name='new_topic'),    
    
    #用于添加新条目的页面
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    
    #用于编辑条目的页面
    path('edit_entry/<int:entry_id>',views.edit_entry,name='edit_entry'), 
    
    #待办事项相关
    path('create_todo/', views.create_todo, name='create_todo'),
    path('update_todo/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
