from django.utils.html import escape
from django.test import TestCase
from django.urls import resolve
from lists.models import Item
from lists.views import home_page, get_comment

class ItemViewTest(TestCase):
    def test_home_page_use_correct_func(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_status_code_200(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/', data={'item_text': ''})
        self.assertEqual(Item.objects.count(), 0)

class CommentItemTest(TestCase):
    def test_no_item_displays_correct_comment(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        self.assertIn('Saatnya tidur YEY', response.content.decode())
        self.assertEqual(get_comment(Item.objects.all()), 'Saatnya tidur YEY')

    def test_less_5_item_displays_correct_comment(self):
        Item.objects.create(text='Tugas 1')
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 1)
        self.assertIn('Duh kerjain tuh lumayan', response.content.decode())
        self.assertEqual(get_comment(Item.objects.all()), 'Duh kerjain tuh lumayan')

    def test_5_more_item_displays_correct_comment(self):
        for i in range(5):
            Item.objects.create(text='Tugas ' + str(i))
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 5)
        self.assertIn('Astaghfirullah KERJAIN', response.content.decode())
        self.assertEqual(get_comment(Item.objects.all()), 'Astaghfirullah KERJAIN')
