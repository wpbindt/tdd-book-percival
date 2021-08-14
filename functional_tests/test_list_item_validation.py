from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self) -> None:
        # Edith goes to the home page and accidentally
        # tries to submit an empty list item. She hits
        # Enter on the empty input box.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # the home page refreshes, and there is an error
        # message saying that list items cannot be blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You can\'t have an empty list item'
            )
        )

        # She tries again with some text, which now works
        # (in particular she gets taken to the list page)
        self.browser.find_element_by_id('id_new_item').send_keys('Milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Milk')

        # She tries to submit an empty item again
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You can\'t have an empty list item'
            )
        )

        # She tries again but with valid input
        self.browser.find_element_by_id('id_new_item').send_keys('Tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Milk')
        self.wait_for_row_in_list_table('2: Tea')
