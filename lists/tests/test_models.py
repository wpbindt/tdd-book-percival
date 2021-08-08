from django.test import TestCase

from lists.models import List, Item


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