"""
URL configuration for ll_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

# URL配置文件，用于ll_project项目。

# `urlpatterns`列表将URL路由到视图。有关更多信息，请参见：
# https://docs.djangoproject.com/en/5.0/topics/http/urls/

# 示例:
# 函数视图
# 1. 添加导入: from my_app import views
# 2. 添加一个URL到urlpatterns: path('', views.home, name='home')
# 基于类的视图
# 1. 添加导入: from other_app.views import Home
# 2. 添加一个URL到urlpatterns: path('', Home.as_view(), name='home')
# 包含另一个URL配置
# 1. 导入包含()函数: from django.urls import include, path
# 2. 将一个URL添加到urlpatterns: path('blog/', include('blog.urls'))
    
    
"""
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',include('learning_logs.urls')),
]
