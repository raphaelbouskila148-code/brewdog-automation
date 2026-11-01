import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class BarLocatorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    __SEARCH_BOX = "#bar-search-input"
    __BAR_NAMES = "main .bar-card-title:visible"
    __EMPTY_MESSAGE = "main .bar-locator-empty"

    @allure.step("Open the bar locator")
    def open_bar_locator(self):
        self.open("/pages/bar-locator")

    @allure.step("Search for the city {city}")
    def search(self, city):
        self.fill_text(self.__SEARCH_BOX, city)
        self.page.wait_for_timeout(2000)

    def get_bar_names(self):
        return self.get_all_texts(self.__BAR_NAMES)

    @allure.step("Check if a bar in {city} is listed")
    def has_bar_in_city(self, city):
        for name in self.get_bar_names():
            if city.lower() in name.lower():
                return True
        return False

    def get_empty_message(self):
        self.wait_for(self.__EMPTY_MESSAGE)
        return self.get_text(self.__EMPTY_MESSAGE)
