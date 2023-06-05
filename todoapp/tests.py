from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Task
class TasklistTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
        username='testuser',
        email='test@email.com',
        password='secret'
        )
        self.task = Task.objects.create(
        title='Test title',
        author=self.user,
        )
    def test_string_representation(self):
        task = Task(title='test task')
        self.assertEqual(str(task), task.title)
    def test_post_content(self):
        self.assertEqual(f'{self.task.title}', 'Test title')
        self.assertEqual(f'{self.task.author}', 'testuser')
    def test_post_list_view(self):
        response = self.client.get(reverse('task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task.html')
    def test_post_detail_view(self):
        response = self.client.get('/task/1/')
        no_response = self.client.get('/task/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'task_detail.html')
