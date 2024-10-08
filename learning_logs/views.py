import re
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry, TodoItem 
from .forms import TopicForm, EntryForm, TodoItemForm  
from django.http import Http404
import requests
from markdown2 import markdown

def index(request):
    """显示主页"""
    github_url = "https://raw.githubusercontent.com/tillywong153111/recordeverything/master/daibanshixiang.md"
    response = requests.get(github_url)
    
    if response.status_code == 200:
        md_content = response.text
        # 保留 `- []` 后有内容的行，去除 `- []` 后无内容的行
        def clean_md_line(line):
            if re.match(r'- \[\] .*', line):
                return line  # 保留 `- []` 后有内容的行
            elif re.match(r'- \[\]', line):
                return None  # 去除 `- []` 后无内容的行
            return line
        
        def clean_md_line(line):
            # 检查`- []`后面是否有内容
            if re.match(r'- \[\] .+', line):
                return line  # 如果`- []`后面有内容，则保留该行
            elif re.match(r'- \[\]\s*$', line):
                return None  # 如果`- []`后面没有内容（仅有空白字符或没有字符），则不保留该行
            return line


        md_lines = md_content.splitlines()
        cleaned_md_lines = [line for line in map(clean_md_line, md_lines) if line is not None]
        cleaned_md_content = '\n'.join(cleaned_md_lines)
        
        html_content = markdown(cleaned_md_content)
    else:
        html_content = "<p>无法加载数据，请稍后再试。</p>"
    
    if request.user.is_authenticated:
        todo_items = TodoItem.objects.filter(owner=request.user)
        context = {'todo_items': todo_items, 'content': html_content}
    else:
        context = {'content': html_content}
        
    return render(request, 'learning_logs/index.html', context)

@login_required
def topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by("-date_added")
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

# 待办事项相关
@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.owner = request.user
            new_todo.save()
            return redirect('learning_logs:index')
    else:
        form = TodoItemForm()
    return render(request, 'learning_logs/create_todo.html', {'form': form})

@login_required
def update_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:index')
    else:
        form = TodoItemForm(instance=todo)
    return render(request, 'learning_logs/update_todo.html', {'form': form})

@login_required
def delete_todo(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.delete()
    return redirect('learning_logs:index')
