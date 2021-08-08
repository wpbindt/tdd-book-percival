from selenium.webdriver.common.keys import Keys
import time

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        window_width = 1024
        ## Not a clue why, but removing either of the next two lines
        ## results in the window not being resized at all
        self.browser.set_window_size(window_width, 768)
        time.sleep(0.1)
        self.browser.set_window_size(window_width, 768)
        time.sleep(1)

        # She notices the input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=10
        )

        # She adds an item to her to do list
        inputbox.send_keys('New item!')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: New item!')

        # She notices that on the list-specific page, the input box
        # is still nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=10
        )
