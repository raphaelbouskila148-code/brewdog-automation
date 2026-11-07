import allure
from playwright.sync_api import Page
from pages.brewdog_page import BrewDogPage


class LoginPage(BrewDogPage):
    def __init__(self, page: Page):
        super().__init__(page)

    __EMAIL_FIELD = "#customer-authentication-web-email"
    __CONTINUE_BTN = "form:has(#customer-authentication-web-email) button[type='submit'][aria-label='Continue']"
    __ERROR_MESSAGE = "#error-for-customer-authentication-web-email"

    @allure.step("Open the sign-in page")
    def open_login(self):
        self.open_without_age_check("/account")
        self.wait_for(self.__EMAIL_FIELD)

    @allure.step("Type the email '{email}' and click Continue")
    def submit_email(self, email):
        self.fill_text(self.__EMAIL_FIELD, email)
        self.click(self.__CONTINUE_BTN)

    def is_email_field_visible(self):
        return self.is_visible(self.__EMAIL_FIELD)

    def is_continue_button_visible(self):
        return self.is_visible(self.__CONTINUE_BTN)

    def get_error(self):
        self.wait_for(self.__ERROR_MESSAGE)
        return self.get_text(self.__ERROR_MESSAGE)
