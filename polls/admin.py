# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Question,Choice

class ChoiceInline(admin.StackedInline):
    #Choice 对象要在 Question 后台页面编辑。默认提供 3 个足够的选项字段
    model = Choice
    #三个关联的选项插槽——由 extra 定义
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #修改使得 "Publication date" 字段显示在 "Question" 字段之前
    # fields = ['pub_date','question_text']

    # fieldsets元组中的第一个元素是字段集的标题。
    # fieldsets = [
    #     (None,              {'fields':['question_text']}),
    #     ('Date information',{'fields':['pub_date']}),
    # ]
    fieldsets = [
        (None,              {'fields':['question_text']}),
        ('Date information',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]


#创建一个模型后台类，接着将其作为第二个参数传给 admin.site.register() ——在你需要修改模型的后台管理选项时这么做。
admin.site.register(Question,QuestionAdmin)






