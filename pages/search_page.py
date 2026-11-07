import allure
from playwright.sync_api import Page
from pages.brewdog_page import BrewDogPage


class SearchPage(BrewDogPage):
    def __init__(self, page: Page):
        super().__init__(page)

    __HEADING = ".search-header__title"
    __PRODUCT_LINK = "main a[href*='/products/']"
    __FIRST_PRODUCT = "main a[href*='/products/'] >> nth=0"
    __NO_RESULTS_MESSAGE = "main :text('No results') >> nth=0"

    @allure.step("Open the search results for {text}")
    def open_search(self, text):
        self.open("/search?q=" + text + "&type=product")

    def get_heading(self):
        return self.get_text(self.__HEADING)

    @allure.step("Count the products in the results")
    def get_products_count(self):
        self.wait_for(self.__FIRST_PRODUCT)
        count = self.count(self.__PRODUCT_LINK)
        self.add_log("Product links found", count)
        return count

    def get_no_results_message(self):
        self.wait_for(self.__NO_RESULTS_MESSAGE)
        return self.get_text(self.__NO_RESULTS_MESSAGE)
