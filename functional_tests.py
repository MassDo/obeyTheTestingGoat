import unittest
from selenium import webdriver

class HomePageTest(unittest.TestCase):

    def setUp(self):
        """
        Actions before each test.
        """
        self.brow = webdriver.Firefox()

    def tearDown(self):
        """
        Actions after each test.
        """
        self.brow.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.brow.get('http://localhost:8000')

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

        table = self.brow.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any( "1: Buy peacock feathers" in row.text for row in rows )
        )

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.


        # Satisfied, she goes back to sleep
        self.fail('permet de faire échouer le test volontairement. Fini le test !')
        
if __name__ == '__main__':
    unittest.main()