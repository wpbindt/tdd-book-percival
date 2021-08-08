from unittest import skip

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self) -> None:
        # Edith goes to the home page and accidentally
        # tries to submit an empty list item. She hits
        # Enter on the empty input box.

        # the home page refreshes, and there is an error
        # message saying that list items cannot be blank

        # She tries again with some text, which now works
        # (in particular she gets taken to the list page)

        # She tries to submit an empty item again

        # She receives a similar warning on the list page
        self.fail('write me!')
