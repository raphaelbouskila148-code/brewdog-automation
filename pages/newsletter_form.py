import allure
from playwright.sync_api import Page
from pages.brewdog_page import BrewDogPage


class NewsletterForm(BrewDogPage):
    def __init__(self, page: Page):
        super().__init__(page)

    __FIRST_NAME_FIELD = "form#contact_form input[name='contact[first_name]']"
    __EMAIL_FIELD = "form#contact_form input[name='contact[email]']"
    __JOIN_BTN = "form#contact_form button:has-text('Join Free Now')"

    @allure.step("Fill the form with name '{first_name}' and email '{email}' and click Join")
    def fill_form(self, first_name, email):
        self.fill_text(self.__FIRST_NAME_FIELD, first_name)
        self.fill_text(self.__EMAIL_FIELD, email)
        self.click(self.__JOIN_BTN)

    def is_first_name_visible(self):
        self.wait_for(self.__FIRST_NAME_FIELD)
        return self.is_visible(self.__FIRST_NAME_FIELD)

    def is_email_visible(self):
        self.wait_for(self.__EMAIL_FIELD)
        return self.is_visible(self.__EMAIL_FIELD)

    def is_join_button_visible(self):
        self.wait_for(self.__JOIN_BTN)
        return self.is_visible(self.__JOIN_BTN)

    @allure.step("Read the browser message of the first name field")
    def get_first_name_message(self):
        message = self.page.locator(self.__FIRST_NAME_FIELD).evaluate("el => el.validationMessage")
        self.add_log("Browser message for the first name", message)
        return message

    @allure.step("Read the browser message of the email field")
    def get_email_message(self):
        message = self.page.locator(self.__EMAIL_FIELD).evaluate("el => el.validationMessage")
        self.add_log("Browser message for the email", message)
        return message
