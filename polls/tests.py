from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone

from .models import Question
from django.urls import reverse

##测试model
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        #创建一个 pub_date 时未来某天的 Question 实例
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        #检查它的 was_published_recently() 方法的返回值——它 应该 是 False
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)



#测试视图：Django 提供了一个供测试使用的 lient 来模拟用户和视图层代码的交互。我们能在 tests.py 甚至是 shell 中使用它。

def create_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available. ")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        ctreate_question(question_text="Past question",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Future quetion",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.",days=-30)
        create_question(question_text="Future_question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_quetion_list'],
            ['<Question: Past question.']
        )

    def test_two_past_question(self):
        create_question(question_text="Past quetion 1.",days=-30)
        create_question(question_text="Past question 2.",days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question2.','<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past question.',days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)