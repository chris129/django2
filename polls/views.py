# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from .models import  Question,Choice
from django.urls import reverse
from django.views import generic



###修改使用通用视图，修改view

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
    #每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供
    model = Question
    template_name = 'polls/detail.html'



class ResultsView(generic.DetailView):
    #DetailView 期望
    # 从 URL 中捕获名为 "pk" 的主键值，所以我们为通用视图把 question_id 改成 pk
    model = Question
    template_name = 'polls/results.html'




def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #polls:results 里面的results取得是urls里面的name='results'的值viewname，其方法见源码会进行旋转results，最后url为
        #polls/question_id/results
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,),current_app='polls'))




# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return render(request,'polls/index.html',context)
#
#
# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
#
#
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         #polls:results 里面的results取得是urls里面的name='results'的值viewname，其方法见源码会进行旋转results，最后url为
#         #polls/question_id/results
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,),current_app='polls'))


