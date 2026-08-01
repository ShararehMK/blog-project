from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogPostTest(TestCase):

    # def setUp(self) -> None:
    #     self.user = User.objects.create(username="hadi")
    #     self.post1 = Post.objects.create(
    #         title = 'post1',
    #         text = 'description of post1',
    #         status = Post.STATUS_CHOICES[0][0],
    #         author = self.user,
    #     )
    #     self.post2 = Post.objects.create(
    #         title = 'post2',
    #         text = 'description of post2',
    #         status = Post.STATUS_CHOICES[1][0],
    #         author = self.user,
    # 
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="hadi")
        cls.post1 = Post.objects.create(
            title = 'post1',
            text = 'description of post1',
            status = Post.STATUS_CHOICES[0][0],
            author = cls.user,
        )
        cls.post2 = Post.objects.create(
            title = 'post2',
            text = 'description of post2',
            status = Post.STATUS_CHOICES[1][0],
            author = cls.user,
        )

    def test_post_model_str_of_title(self):
        post = self.post2
        self.assertEqual(str(post), f'Title: {post.title}')

    def test_post_list_url(self):
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_title_show_on_post_list(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response=self.client.get(f'/blog/{self.post1.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_title_show_on_post_detail(self):
        # response = self.client.get(f'/blog/{self.post1.pk}/')
        response = self.client.get(reverse('post_detail' , args=[self.post1.pk]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')

    def test_status_code_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_on_post_list(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_url(self):
        response= self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_by_name(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'some title',
            'text': 'some text',
            'status': 'pub',
            'author': self.user.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'some title')
        self.assertEqual(Post.objects.last().text, 'some text')

    def test_post_update_url(self):
        response = self.client.get(f'/blog/{self.post1.pk}/update/')
        self.assertEqual(response.status_code, 200)

    def test_post_update_url_by_name(self):
        response = self.client.get(reverse('post_update' , args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_url(self):
        response = self.client.get(f'/blog/{self.post1.pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_post_delete_url_by_name(self):
        response = self.client.get(reverse('post_delete', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post1.pk]),{
            'title': 'updated title of post1',
            'text': 'updated text of post1',
            'status': 'pub',
            'author': self.post1.author.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.first().title, 'updated title of post1')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 302)