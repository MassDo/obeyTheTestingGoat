import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 1

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        """
        Actions before each test.
        """
        self.brow = webdriver.Firefox()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:    
                table = self.brow.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [r.text for r in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        """
        Actions after each test.
        """
        self.brow.quit()

    def test_can_start_a_list_and_retrieve_it_later_one_user(self):
        
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.brow.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.brow.title)
        header = self.brow.find_element_by_tag_name('h1').text
        self.assertIn('Start a new to-do list !', header)

        # She is invited to enter a to-do item straight away
        inputbox = self.brow.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox = self.brow.find_element_by_id('id_new_item')
        inputbox.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')      

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.brow.find_element_by_id('id_new_item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # self.fail('Fini le test !')
        # She visits that URL - her to-do list is still there.


        # Satisfied, she goes back to sleep
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith start a new todo list
        self.brow.get(self.live_server_url)
        inputbox = self.brow.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that the list has a unique URL
        edith_list_url = self.brow.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user comes along the site (Francis)

        ## We use a new browser session to make 
        ## sure that no informations of edith's
        ## is coming throught from cookies etc ...
        self.brow.quit()
        self.brow = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.brow.get(self.live_server_url)
        page_text = self.brow.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.brow.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own URL
        francis_list_url = self.brow.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        
        # Again, there is no trace of Edith's list
        ## POST of francis could send post data of edith ?
        page_text = self.brow.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        # Edith goes to the home page she notice a nicely centered inputbox
        self.brow.get(self.live_server_url)
        ## define the window's size in order to check if
        ## the inputbox is centered
        self.brow.set_window_size(1024, 768)
        inputbox = self.brow.find_element_by_id('id_new_item')
        ## Centered ?
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # Then she adds an item to the inputbox and press Enter to validate...
        inputbox.send_keys('testing item')
        inputbox.send_keys(Keys.ENTER) ## => add item and create list via POST 
                                       ## at /lists/new 
                                       ## then redirect to /lists/<list_id>/
        # She sees her item added to the page and the inputbox is still centered !
        self.wait_for_row_in_list_table('1: testing item')
        ## new inputbox var because it a new page
        inputbox = self.brow.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
