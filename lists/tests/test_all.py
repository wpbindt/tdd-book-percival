from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.clien        self.wait_for_row_in_list_table('1: Milk')t.get(f'/lists/{list_.id}/')
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


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_lists(self):
        first_list = List()
        first_list.save()

        second_list = List()
        second_list.save()

        saved_lists = List.objects.all()
        first_saved_list = saved_lists[0]
        second_saved_list = saved_lists[1]
        self.assertEqual(first_saved_list, first_list)
        self.assertEqual(second_saved_list, second_list)

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


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
