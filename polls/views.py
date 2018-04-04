# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import  Question
from django.template import loader
from django.http import Http404


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return HttpResponse(template.render(context,request))


#使用renter重新index,The render() function takes the request object as its first argument, a template name as its second
# argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template
# rendered with the given context.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list':latest_question_list,
    }
    return render(request,'polls/index.html',context)


# def detail(request,question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         #自定义错误打印信息
#         raise Http404("Question does not exist")
#     return render(request,'polls/detail.html',{'question':question})

#使用get_object_or_404快捷函数替换上面的404
def detail(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})


def results(request,question_id):
    response = "You're looking at the results of question %s ."
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse("You're voting on question %s ." % question_id)



