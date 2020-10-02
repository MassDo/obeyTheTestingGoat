from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

from lists.models import Item, List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListViewTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new',
        data = {
            "item_text": "A new list item"
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_a_POST(self):
        response = self.client.post('/lists/new',
        data = {
            "item_text": "A new list item"
        })
        list_ = List.objects.first()
        self.assertRedirects(response,f'/lists/{list_.id}/')


class NewItemViewTest(TestCase):


    def test_can_save_POST_request_to_existing_list(self):
        # database implementation
        another_list = List.objects.create()
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/add_item', data = {
            "item_text": "A new list item for list_",      
        })

        # retrieve data from orm and test logic
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, "A new list item for list_")
        self.assertEqual(item.list, list_)

    def test_redirects_to_list_view(self):
        # data implementation
        another_list = List.objects.create()
        list_ = List.objects.create()

        response = self.client.post(f'/lists/{list_.id}/add_item',
        data = {
            "item_text": "A new list item for list_"
        })

        self.assertRedirects(response, f'/lists/{list_.id}/')

    


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        # Feed database
        list_ = List.objects.create()
        Item.objects.create(text='item_1', list=list_)
        Item.objects.create(text='item_2', list=list_)
        other_list_ = List.objects.create()
        Item.objects.create(text='other item_1', list=other_list_)
        Item.objects.create(text='other item_2', list=other_list_)

        # Actions
        response = self.client.get(f'/lists/{list_.id}/')

        # Logic tested
        self.assertContains(response, 'item_1')
        self.assertContains(response, 'item_2')
        self.assertNotContains(response, 'other item_1')
        self.assertNotContains(response, 'other item_2')

    def test_passes_correct_list_to_the_template(self):
        # faire 2 liste
        # en passer une a la vue view_list vie lurl /lists/pk_list/ via POST
        # vérifier que la reponse du client contient la bonne liste (l'obj)
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        response = self.client.post(f'/lists/{list_2.id}/')

        self.assertEqual(response.context['list_'], list_2)



class ListAndItemModelTest(TestCase):    

    def test_saving_and_retrieving_items(self):
        # Feed the model.
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first item of the list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        # Get data from models Item and List and test if same as data feed.
        ## If it passe, model are implemented.
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first item of the list item')
        self.assertEqual(first_saved_item.list, saved_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, saved_list)


