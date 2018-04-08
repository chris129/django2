# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Question,Choice

class ChoiceInline(admin.TabularInline):
    #关联对象以一种表格式的方式展示，显得更加紧凑
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #以列的形式展示
    list_display = ('question_text','pub_date','was_published_recently')
    inlines = [ChoiceInline]
    #添加了一个“过滤器”侧边栏，允许人们以 pub_date 字段来过滤列表
    list_filter = ['pub_date']
    #增加一个搜索框。当输入待搜项时，Django 将搜索 question_text 字段
    search_fields = ['question_text']


#创建一个模型后台类，接着将其作为第二个参数传给 admin.site.register() ——在你需要修改模型的后台管理选项时这么做。
admin.site.register(Question,QuestionAdmin)






