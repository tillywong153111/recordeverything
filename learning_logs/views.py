from django.shortcuts import render, redirect  # 从 django.shortcuts 模块中导入 render 和 redirect 函数
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry  # 从当前目录的 models.py 文件中导入 Topic 类
from .forms import TopicForm, EntryForm  # 从当前目录的 forms.py 文件中导入 TopicForm 类
from django.http import Http404




def index(request):  # 定义 index 视图函数，该函数处理对应的 HTTP 请求
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')  # 返回一个渲染后的 HTML 页面

@login_required
def topics(request):  # 定义 topics 视图函数，该函数处理对应的 HTTP 请求
    """显示所有主题"""
    #topics = Topic.objects.order_by('date_added')  # 从数据库中获取所有 Topic 对象，并按 date_added 字段排序
    topics = Topic.objects.filter(owner=(request.user)).order_by('date_added')
    context = {'topics': topics}  # 创建一个字典，用于传递给模板
    return render(request, 'learning_logs/topics.html', context)  # 返回一个渲染后的 HTML 页面，该页面显示所有的主题

@login_required
def topic(request, topic_id):  # 定义 topic 视图函数，该函数处理对应的 HTTP 请求
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)  # 从数据库中获取给定 id 的 Topic 对象
    #确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
        
    entries = topic.entry_set.order_by("-date_added")  # 获取该主题下的所有条目，并按 date_added 字段逆序排序
    context = {'topic': topic, 'entries': entries}  # 创建一个字典，用于传递给模板
    return render(request, 'learning_logs/topic.html', context)  # 返回一个渲染后的 HTML 页面，该页面显示单个主题及其所有的条目




@login_required
def new_topic(request):  # 定义 new_topic 视图函数，该函数处理对应的 HTTP 请求
    """添加新主题"""
    if request.method != 'POST':  # 如果 HTTP 请求的方法不是 POST，则创建一个新表单
        form = TopicForm()  # 创建一个空的 TopicForm 对象
    else:  # 如果 HTTP 请求的方法是 POST，则处理提交的数据
        form = TopicForm(data=request.POST)  # 创建一个 TopicForm 对象，并用 POST 提交的数据填充该对象
        if form.is_valid():  # 如果表单数据有效，则保存数据
            #form.save()  # 保存表单数据到数据库
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')  # 重定向到 topics 视图

    # 显示空表单或指出表单数据无效
    context = {'form': form}  # 创建一个字典，用于传递给模板
    return render(request, 'learning_logs/new_topic.html', context)  # 返回一个渲染后的 HTML 页面，该页面显示空表单或指出表单数据无效


@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # 未提交数据：创建一个空表单
        form = EntryForm()
    else:
        #POST 提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)
     
    #显示空表单或指出表单数据无效
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)


@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #初次请求：使用当前的条目填充表单
        form = EntryForm(instance=entry)
    else:
        #POST 提交的数据：对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    context ={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)


