import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open the homepage")
    def open_home(self):
        self.open("/")

    @allure.step("Open the homepage without confirming the age")
    def open_home_without_age_check(self):
        self.open_without_age_check("/")

    @allure.step("Read the address of the footer link '{link_text}'")
    def get_footer_link_address(self, link_text):
        return self.get_attribute("footer a:has-text('" + link_text + "') >> nth=0", "href")
