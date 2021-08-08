from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_in_chosen_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        other_list = List.objects.create()
        Item.objects.create(text='I should not appear', list=other_list)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'I should not appear')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        list_ = List.objects.create()

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertEqual(response.context['list'], list_)

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_redirects_after_POST(self):
        other_list = List.objects.create()
        list_ = List.objects.create()

        response = self.client.post(
            f'/lists/{list_.id}/add_item',
            data={'item_text': 'item text'}
        )

        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_POST_adds_item_to_list(self):
        other_list = List.objects.create()
        list_ = List.objects.create()

        self.client.post(
            f'/lists/{list_.id}/add_item',
            data={'item_text': 'item text'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'item text')
        self.assertEqual(new_item.list, list_)
