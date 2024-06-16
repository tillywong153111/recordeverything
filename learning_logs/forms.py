# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:04:08 2024

@author: MSI
"""

from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}
    
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}