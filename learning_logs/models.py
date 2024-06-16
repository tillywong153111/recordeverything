

# 导入 Django 的模型模块，这是创建 Django 模型的基础
from django.db import models
from django.contrib.auth.models import User


# 创建你的模型在这里

# 定义一个名为 Topic 的模型，该模型继承自 models.Model，这是创建所有 Django 模型的基础
class Topic(models.Model):
    """用户学习的主题"""
    
    # 定义一个名为 text 的字段，它的类型是 CharField，这是一个用于存储字符串的字段类型。max_length=200 表示这个字段最多可以存储 200 个字符
    text = models.CharField(max_length=200)
    
    # 定义一个名为 date_added 的字段，它的类型是 DateTimeField，这是一个用于存储日期和时间的字段类型。auto_now_add=True 表示当创建一个新的 Topic 对象时，这个字段会自动设置为当前的日期和时间
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    # 定义了模型的 __str__ 方法，这是一个特殊的方法，当需要将 Topic 对象转换为字符串时，Django 会调用这个方法
    def __str__(self):
        """返回模型的字符串表示"""
        
        # 这个方法返回 topic 的 text 字段，这意味着当我们打印一个 Topic 对象时，我们会看到它的 text 字段的内容
        return self.text

class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """返回一个表示条目的简单字符串"""
        if len(self.text) >50:
            return f"{self.text[:50]}..."
        else:
            return self.text