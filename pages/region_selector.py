import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class RegionSelector(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    __COUNTRY_SELECT = "select[js-country-selector='select']"

    def get_selected_country(self):
        return self.get_value(self.__COUNTRY_SELECT)

    @allure.step("Choose the country {country_code} and wait for the new store")
    def choose_country(self, country_code):
        self.select_option(self.__COUNTRY_SELECT, country_code.lower())
        for i in range(15):
            if "usa.brewdog.com" in self.url:
                self.page.wait_for_timeout(1000)
        self.add_log("New address", self.url)
