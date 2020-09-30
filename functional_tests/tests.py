import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        """
        Actions before each test.
        """
        self.brow = webdriver.Firefox()

    def check_for_row_in_rows_table(self, row_text):

        table = self.brow.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [r.text for r in rows])
        

    def tearDown(self):
        """
        Actions after each test.
        """
        self.brow.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.brow.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.brow.title)
        header = self.brow.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header)

        # She is invited to enter a to-do item straight away
        inputbox = self.brow.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_rows_table("1: Buy peacock feathers")       

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.brow.find_element_by_id('id_new_item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_rows_table("1: Buy peacock feathers")
        self.check_for_row_in_rows_table("2: Use peacock feathers to make a fly")
        
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.


        # Satisfied, she goes back to sleep
        self.fail('Fini le test !')
